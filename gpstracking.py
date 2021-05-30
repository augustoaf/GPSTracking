import serial
import time
import datetime
import sys

serial_port = serial.Serial ("/dev/ttyS0")
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

def write_to_file(is_new_file, content):
    file_name = "coordinates.txt"
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
    
try:
    write_to_file(True, "")

    while True:
        try:
            #read NMEA string received
            received_data = (str)(serial_port.readline()) 
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
                
                #print("NMEA Time: ", nmea_time,"\n")
                
                #write GPS coordinates in a file
                current_date_and_time = datetime.datetime.now()
                content = str(current_date_and_time) + "," + latitude + "," + longitude 
                write_to_file(False, content)
                time.sleep(15)
        except Exception as e:
            #print(f"Logging exception as str: {e}")
            error = f"Logging exception as repr: {e!r}"
            write_to_file(False, error)
            time.sleep(5)

except KeyboardInterrupt:
    sys.exit(0)
