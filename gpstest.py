#read GPS coordinates directly from serial port
import serial
import sys

ser = serial.Serial ("/dev/ttyS0")
try:
    while True:
        received_data = (str)(ser.readline()) #read NMEA string received
        print(received_data, "\n")
except KeyboardInterrupt:
    sys.exit(0)

