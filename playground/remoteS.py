from inputs import get_gamepad
import socket
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0',6666))
s.listen(1)
conn,addr=s.accept()
prevB=0
print('accept from ',addr)
beginTime = time.perf_counter()
sndx=''
sndr=''
while True:
    events = get_gamepad()
    for event in events:
        # print(event.ev_type, event.code, event.state)
        if event.code=='ABS_X':
            degree=int(event.state/1024)
            if degree > 0:
                real = (-1.554*degree)+89.2066
            else:
                real = -(1.95*degree)+92
            sndx='X'+str(int(real))+'\n'
            conn.send(sndx.encode())
        if event.code=='ABS_Y':
            snd='Y'+str(int(event.state/512))+'\n'
            # conn.send(snd.encode())
            
        if event.code=='ABS_RZ':
            sndr='R'+str(event.state)+'\n'
            print(sndr)
            conn.send(sndr.encode())
        if event.code=='ABS_Z':
            snd='L'+str(event.state)+'\n'
            # conn.send(snd.encode())
        if event.code=='BTN_EAST':
            if event.state==0 and prevB==1:
                conn.send('close'.encode())
                conn.close()
                exit(0)
            else:
                prevB=event.state
    # if time.perf_counter()-beginTime>0.2:
        
        
    #     beginTime = time.perf_counter()   
    # data=conn.recv(1024)
    # print(data)
    