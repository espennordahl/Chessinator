# Chessinator

Software for my arduino based automagic chess board. It's still very much work in progress, but slowly coming together.

Current hardware:
- Makebloc xy plotter kit v2.02<br>
Controls the motors and magnet component for moving pieces around. Uses the Me Orion micro controller, based on Arduino UNO.

- Raspberry Pi 3 model B<br>
Runs the chess software, receives sensor input and sends commands to the Orion through USB serial communication.

Software/firmware modules:
- Chessberry Py<br>
Chess game logic module running on the raspberry Pi. 

- GCodeParser<br>
Firmware for the xy plotter microcontroller. Almost unchanged from the firmware that comes with the Makeblock assembly instructions. Accepts standard GCode using serial communication. 

TODO: 
- Extend xy plotter with electro magnet.
- Write plotter control module for raspberry.
- Write base event loop for raspberry.
- Add electro manget (servo?) functionality to Orion firmware.
