from inputs import get_gamepad
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0',6666))
s.listen(1)
conn,addr=s.accept()
print('accept from ',addr)
while 1:
    events = get_gamepad()
    for event in events:
        print(event.ev_type, event.code, event.state)
        if event.code=='ABS_X':
            snd='XX'+str(event.state)
            conn.send(snd.encode())
        if event.code=='ABS_Y':
            snd='YY'+str(event.state)
            conn.send(snd.encode())
        if event.code=='ABS_RZ':
            snd='RT'+str(event.state)
            conn.send(snd.encode())
        if event.code=='ABS_Z':
            snd='LT'+str(event.state)
            conn.send(snd.encode())
    # data=conn.recv(1024)
    # print(data)
    