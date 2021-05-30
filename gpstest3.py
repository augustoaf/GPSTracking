import serial
import time
import string
import pynmea2

while True:
	port="/dev/ttyS0"
	ser=serial.Serial(port, baudrate=9600, timeout=0.5)
	dataout = pynmea2.NMEAStreamReader()
	data=ser.readline()

	newdata=data.decode('utf-8')
	if newdata[0:6] == "$GPRMC":

		#print("inside")
		newmsg=pynmea2.parse(newdata)
		lat="%.4f" %(newmsg.latitude)
		lng="%.4f" %(newmsg.longitude)
		gps = str(lat) + "," + str(lng)
		print(gps)
		time.sleep(15)

