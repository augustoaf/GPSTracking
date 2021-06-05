gpstracking app  
App using GPS "GY-NEO6MV2" sensor attached to a Raspberry PI 4. This app get coordinates using NMEA protocol directly from serial port and publish to a MQTT topic.

IMPROVEMENT: make the serial port reading a thread and keep the last "serial.readline data" accessible to the entire app.

Tip0: First usage of GPS did not get coordinates from the route when I ride with the device/sensor (it was getting the same GPS coordinates where I first turn-on the device). I keep the device/sensor turned on for 12 hours and then I did a new ride, then it traced the route. TO DO: Need to investigate this behavior.  
Tip1: coordinates from GPS can be read directly from the serial port (ttyS0), try cat /dev/ttyS0, but if you disable the "serial login shell" (which you are suppose to disable due the same port usage as the sensor) you will not be able to see the output.  
Tip2: as the battery (in the sensor) retains clock and last position, time to first fix (TTFF) significantly reduces to 1s. This allows much faster position locks, although, according sensor spec, the TTFF in "cold" configuration may take until 32s for "first fix".  
Tip3: if you want to run this app in background and detached from the terminal, use "sudo nohup [app] &"  

Requirements:  
-enable uart port adding this line (enable_uart=1) at the end of /boot/config.txt and then reboot the RPI. After reboot check if the /dev/ttyS0 exists (you can check also through /dev/serial0 or /dev/serial1) and using picocom (apt-get install picocom) check if the ttyS0 baudrate is set to 9600 (if not change it).  
-use raspi-config to disable "serial login shell" and enable serial interface (hardware)  
-pip3 install paho-mqtt  

References:  
https://www.engineersgarage.com/microcontroller-projects/articles-raspberry-pi-neo-6m-gps-module-interfacing/  
https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/  