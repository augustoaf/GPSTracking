import serial
import time
import datetime
import sys
import paho.mqtt.client as mqtt 

serial_port = serial.Serial ("/dev/ttyS0", timeout=1)
gpgga_info = "$GPGGA,"

def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    #fix added by Augusto
    position = position * -1
    position = "%.4f" %(position)
    return position

def write_coordinates_to_file(is_new_file, content):
    file_name = "coordinates.txt"
    write_to_file(is_new_file, content, file_name) 

def write_gga_to_file(is_new_file, content):
    file_name = "gga.txt"
    write_to_file(is_new_file, content, file_name)

def write_to_file(is_new_file, content, file_name):
    file = ""
    #parameter "a" will append new content at the end of the file, "w" will overwrite the previous file content - both will create a file if it does not exists.
    if is_new_file:
        file = open(file_name, "w")
    else:
        file = open(file_name, "a")
    content = content + "\n"
    file.write(content)
    file.close()
    print(content)

def instantiate_mqtt_client():
    client = ""
    try:
        broker_address="192.168.86.42"        
        client = mqtt.Client("id-1")
        client.connect(broker_address, port=1883, keepalive=20)
    except Exception as e:
        error = f"MQTT Client: Logging exception as repr: {e!r}"
        write_to_file(False, error)
            
    return client

def send_message(mqtt_client, payload):
    if not isinstance(mqtt_client, str):
        try:
            broker_topic = "satellite/gps"
            mqtt_client.publish(broker_topic,payload)
        except Exception as e:
            error = f"MQTT Publish: Logging exception as repr: {e!r}"
            write_to_file(False, error)

try:
    write_coordinates_to_file(True, "")#create an empty log file
    write_gga_to_file(True, "")#create an empty log file
    mqtt_client = instantiate_mqtt_client()
    date_to_wait = datetime.datetime.now()

    while True:
        try:
            #read NMEA string received
            received_data = (str)(serial_port.readline()) 
            
            if (datetime.datetime.now() > date_to_wait):
                #check for NMEA GPGGA string
                GPGGA_data_available = received_data.find(gpgga_info)   

                if (GPGGA_data_available>0):
                    #read and store data after “$GPGGA,” string
                    GPGGA_buffer = received_data.split(gpgga_info,1)[1]  
                    NMEA_buff = (GPGGA_buffer.split(","))
                    nmea_time = []
                    nmea_latitude = []
                    nmea_longitude = []
                    nmea_time = NMEA_buff[0]                    
                    nmea_latitude = NMEA_buff[1]                
                    nmea_longitude = NMEA_buff[3]               
                    latitude = (float)(nmea_latitude)
                    latitude = convert_to_degrees(latitude)
                    longitude = (float)(nmea_longitude)
                    longitude = convert_to_degrees(longitude)
                                
                    #write GPS coordinates in a file
                    current_date_and_time = datetime.datetime.now()
                    content = str(current_date_and_time) + "," + nmea_time + "," + latitude + "," + longitude 
                    write_coordinates_to_file(False, content)
                    write_gga_to_file(False, str(current_date_and_time) + "," + received_data)
                    #publish mqtt message
                    send_message(mqtt_client, content)
                    date_to_wait = datetime.datetime.now() + datetime.timedelta(0,15)
        except Exception as e:
            error = f"GPS Coordinates: Logging exception as repr: {e!r}"
            write_coordinates_to_file(False, error)
            date_to_wait = datetime.datetime.now() + datetime.timedelta(0,5)
            
except KeyboardInterrupt:
    serial_port.close()
    sys.exit(0)
