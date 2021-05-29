gpstracking app
App using GPS "GY-NEO6MV2" sensor attached to a Raspberry PI 4. This app get coordinates using NMEA protocol directly from serial port.
Tip1: coordinates from GPS can be get directly from the serial port (ttyS0). Try cat /dev/ttyS0.
Tip2: As the battery (in the sensor) retains clock and last position, time to first fix (TTFF) significantly reduces to 1s. This allows much faster position locks, although, according sensor spec, the TTFF in "cold" configuration may take until 32s for "first fix".
Tip3: The coordinates are in degrees and must add the caracter "-" at the beggining of latitude and longitude.

Requirements:
-enable uart port adding this line (enable_uart=1) at the end of /boot/config.txt and then reboot the RPI. After reboot check if the /dev/ttyS0 exists (you can check also through /dev/serial0 or /dev/serial1) and using picocom (apt-get install picocom) check if the ttyS0 baudrate is set to 9600 (if not change it).

References:
https://www.engineersgarage.com/microcontroller-projects/articles-raspberry-pi-neo-6m-gps-module-interfacing/
https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/