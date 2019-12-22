# Line follow car (demo)

## How to run python script
### x86 PC
1. Use ```anaconda``` to manage the package, you can use ```base``` to run script or create a new environment.
2. Install the follow package (Hint: Use [tsinghua](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/) mirror).  
``` conda install opencv-python pyserial```
3. Edit the serial port name and band rate, such as using ```COM3``` on Windows or ```/dev/tty*``` on Linux.
4. Edit the camera number at line 9, such as 1 or 0.
### Linux on Raspberry
1. Edit serial port to '''/dev/ttyUSB0'''
2. '''python3 xxx.py''' 

## How to use car firmware
0. Open file in Code for car
1. Simple version is maintaining, old version is deprecated. 
2. BURN IT.  