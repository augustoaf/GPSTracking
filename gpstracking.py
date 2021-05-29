import serial
import time
import datetime
import sys

ser = serial.Serial ("/dev/ttyS0")
gpgga_info = "$GPGGA,"
GPGGA_buffer = 0
NMEA_buff = 0

def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position

try:
    #parameter "a" will append new content at the end of the file, "w" will overwrite the previous file content - both will create a file if it does not exists.
    f = open("/home/pi/coordinates.txt", "w")
    f.close()

    while True:
        try:
            received_data = (str)(ser.readline()) #read NMEA string received
            GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string
            if (GPGGA_data_available>0):
                GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after “$GPGGA,” string
                NMEA_buff = (GPGGA_buffer.split(","))
                nmea_time = []
                nmea_latitude = []
                nmea_longitude = []
                nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
                nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
                nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
                #print("NMEA Time: ", nmea_time,"\n")
                lat = (float)(nmea_latitude)
                lat = convert_to_degrees(lat)
                longi = (float)(nmea_longitude)
                longi = convert_to_degrees(longi)
                current_date_and_time = datetime.datetime.now()
                content = str(current_date_and_time) + ",-" + lat + ",-" + longi + "\n"
                print(content)
                f = open("/home/pi/coordinates.txt", "a")
                f.write(content)
                f.close() 
                time.sleep(30)
        except Exception as e:
            #print(f"Logging exception as str: {e}")
            print(f"Logging exception as repr: {e!r}")

except KeyboardInterrupt:
    sys.exit(0)
