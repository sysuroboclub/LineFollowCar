from inputs import get_gamepad
import serial
ser=serial.Serial('COM3',115200)
while 1:
    events = get_gamepad()

    #X,Y [-32768,+32768]
    #Z,RZ(RT,LT) [0,255]
    for event in events:
        # print(event.ev_type, event.code, event.state)
        if event.code=='ABS_X':
            snd='X'+str(int(event.state/512))+'\r'
            ser.write(snd.encode())
        if event.code=='ABS_Y':
            snd='Y'+str(int(event.state/512))+'\r'
            ser.write(snd.encode())
        if event.code=='ABS_RZ':
            snd='R'+str(int(event.state))+'\r'
            ser.write(snd.encode())
        if event.code=='ABS_Z':
            snd='L'+str(int(event.state))+'\r'
            ser.write(snd.encode())
