import socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('192.168.1.74',6666))
while True:
    data=s.recv(128)
    print(data.decode(),len(data))
    