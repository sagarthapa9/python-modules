import os 
import time
from datetime import datetime 
from serial import Serial
import PySimpleGUI as sg

microbit_data = {
    'temp': 0,
    'lightLevel': 0,
}
global layout

def loadData():
    nxtLtlPoll = 0.0
    nxtTmpPoll = 0.0
    serialDevDir='/dev/serial/by-id'
    if ( os.path.isdir(serialDevDir) ):
        serialDevices = os.listdir(serialDevDir) 

        if ( len(serialDevices) > 0 ):

            serialDevicePath = os.path.join(serialDevDir, serialDevices[0])
            serial = Serial(port=serialDevicePath, baudrate=115200, timeout=0.5) 

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
                    
                    elif ( msgType == b'TMP' ):
                           microbit_data['temp'] = msgData.decode('ascii').rstrip()
                           
                    elif ( msgType == b'LTL' ):
                        microbit_data['lightLevel'] = msgData.decode('ascii').rstrip()
                        
                    return microbit_data
                    
                currentTime = time.time() 
                if ( currentTime > nxtLtlPoll ):
                    serial.write(b'LTL:\n' )
                    nxtLtlPoll = currentTime + 5.0
                    
                if(currentTime > nxtTmpPoll):
                    serial.write(b'TMP:\n')
                    nxtTmpPoll = currentTime + 2.0 
                    
                else:

                 print('No serial devices connected') 

        else:

             print('No serial devices connected') 


layout= [[[sg.Text("Light Level")],[sg.Text(microbit_data['lightLevel'],size=(10,2), key='-LTL-')]],[[sg.Text("Room Temp")],[sg.Text(microbit_data['temp'],size=(10,2), key='-TMP-')]],[sg.Button("OK")]]
#Create the window
window = sg.Window("Demo", layout)

# Event loop
while True:
    event,values = window.read(timeout=100)
    res=loadData()
    #print(res)
    
    if event == "OK" or event == sg.WIN_CLOSED:
     break
    else:
     window['-TMP-'].update(res['temp'])
     window['-LTL-'].update(res['lightLevel'])
     
window.close()

                            



