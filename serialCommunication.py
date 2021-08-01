import os 
import time
from datetime import datetime 
from serial import Serial 

nextCompassPoll = 0.0 ;

serialDevDir='/dev/serial/by-id' 

if ( os.path.isdir(serialDevDir) ):
    serialDevices = os.listdir(serialDevDir) 

    if ( len(serialDevices) > 0 ):

        serialDevicePath = os.path.join(serialDevDir, serialDevices[0])

        serial = Serial(port=serialDevicePath, baudrate=19200, timeout=0.2) 

        while( True ):

            receivedMsg = serial.readline() 

            if ( (len(receivedMsg) >= 4) and (receivedMsg[3] == b':'[0])):

                msgType = receivedMsg[0:3] 
                msgData = receivedMsg[4:]

                if ( msgType == b'TIM' ):
                    timeString = datetime.now().strftime('%H:%M') 
                    sendMsg = b'TIM:' + timeString.encode('ascii')
                    serial.write(sendMsg + b'\n')

                elif ( msgType == b'DAT' ):
                    dateString = datetime.now().strftime('%d-%b-%Y') 
                    sendMsg = b'DAT:' + dateString.encode('ascii')
                    serial.write(sendMsg + b'\n')

                elif ( msgType == b'LT' ):
                    print('Compass Bearing = ' + msgData.decode('ascii'))

            currentTime = time.time() 
            if ( currentTime > nextCompassPoll ):
                serial.write(b'CMP:\n')
                nextCompassPoll = currentTime + 2.0
    else:

        print('No serial devices connected') 

else:

    print(serialDevDir + ' does not exist') 