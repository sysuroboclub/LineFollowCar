import socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    s.connect(('192.168.43.85',6666))
except socket.error:
    print(socket.error)
import serial
import time
ser=serial.Serial('/dev/ttyUSB0',115200)
prevB=0
beginTime = time.perf_counter()
data=s.recv(512)
xdata='X95'
rdata='R0'
while True:
    data=s.recv(512)
    if len(data)>0:
        tmp=data.decode()
        if tmp[0]=='X':
            xdata=tmp
        elif tmp[0]=='R':
            rdata=tmp
        elif tmp=='close':
                s.close()
                exit()
    if time.perf_counter()-beginTime>0.2:
        print(xdata,rdata)
        ser.write(xdata.encode())
        beginTime = time.perf_counter()
        ser.write(rdata.encode())