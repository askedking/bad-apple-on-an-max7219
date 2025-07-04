you need:
arduino nano
max7219-dotmatrix-module-v02.
asorted wires
breadboard(optional)

connect:
vcc - 5v
gnd - gnd
din - d11
cs - d10
clk - d13


to run:
1. install the mp4 into downloads
2. copy the mp4 file location and replace the one set in the python files
3. in arduino ide, setup the board(select the correct port, and board type)
4. upload the code to your arduino nano.
5. back in python, change the pre-set(mine was COM7) port to be the port you are using.
6. close ide, and and run the python file, it should play two versions of the video on your pc screen ( original, and 8x8) and the 8x8 version should be playing on your arduino.
7. have fun :)
