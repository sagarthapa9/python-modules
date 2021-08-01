
import PySimpleGUI as sg
import os 
import time
import base64
from datetime import datetime 
from serial import Serial 
import json

sg.ChangeLookAndFeel('lightblue')
BG_COLOR = "#FFC13F" #sg.theme_text_color()
TXT_COLOR = "#000000" #sg.theme_background_color()
ALPHA = 0.8
APP_DATA = {
    'lightLevel':100,
    'roomTemprature':0,
    'Icon': None,
}


def get_Serial_Communication_Data():
    global APP_DATA
    nextCompassPoll = 0.0
    serialDevDir = '/dev/serial/by-id'

    if (os.path.isdir(serialDevDir)):
        serialDevices = os.listdir(serialDevDir)

        if (len(serialDevices) > 0):

            serialDevicePath = os.path.join(serialDevDir, serialDevices[0])

            serial = Serial(port=serialDevicePath, baudrate=19200, timeout=0.2)

            while(True):

                receivedMsg = serial.readline()

                if ((len(receivedMsg) >= 4) and (receivedMsg[3] == b':'[0])):

                    msgType = receivedMsg[0:3]
                    msgData = receivedMsg[4:]
                    if (msgType == b'LTL'):
                       APP_DATA['lightLevel'] = msgData.decode('ascii')
                       print(APP_DATA['lightLevel'])
                    elif(msgType == b'RMTP'):
                        APP_DATA['roomTemprature'] = msgData.decode('ascii')
                        print(APP_DATA['roomTemprature'])
                currentTime = time.time()
                if (currentTime > nextCompassPoll):
                    serial.write(b'CMP:\n')
                    nextCompassPoll = currentTime + 2.0
        else:

            print('No serial devices connected')

    else:

     print(serialDevDir + ' does not exist')

def create_window():
    """ Create the application window """
   
    col1 = sg.Column(
        [[sg.Text('Light Level:', font=('Arial Rounded MT Bold', 18), pad=((10, 0), (50, 0)), size=(18, 1), background_color=BG_COLOR, text_color=TXT_COLOR)],[sg.Text(APP_DATA['lightLevel'], font=('Arial Rounded MT Bold', 18), pad=((10, 0), (50, 0)), size=(18, 1), background_color=BG_COLOR, text_color=TXT_COLOR, key='lightLevel')]],
            background_color=BG_COLOR, key='COL1')
    
    col2 = sg.Column(
        [[sg.Text('×', font=('Arial Black', 16), pad=(0, 0), justification='right', background_color=BG_COLOR, text_color=TXT_COLOR, enable_events=True, key='-QUIT-')],
        [sg.Image(data=APP_DATA['Icon'], pad=((5, 10), (0, 0)), size=(100, 100), background_color=BG_COLOR, key='Icon')]],
            element_justification='center', background_color=BG_COLOR, key='COL2')

    top_col = sg.Column([[col1, col2]], pad=(0, 0), background_color=BG_COLOR, key='TopCOL')

    layout = [[top_col]]

    window = sg.Window(layout=layout, title='Info window', size=(400, 315), margins=(0, 0), finalize=True, 
        element_justification='center', keep_on_top=True, no_titlebar=True, grab_anywhere=True, alpha_channel=ALPHA)

    for col in ['COL1', 'COL2']:
        window[col].expand(expand_y=True, expand_x=True)

    # layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")]]

    # # Create the window
    # window = sg.Window("Demo", layout)
    return window

def main(refresh_rate):
    """ The main program routine """
    timeout_minutes = refresh_rate * (60 * 1000)

    # Try to get the current users ip location
    try:
      get_Serial_Communication_Data()
    except ConnectionError:
        pass

    # Create main window
    window = create_window()

    # Event loop
    while True:
        event, _ = window.read(timeout=timeout_minutes)
        if event in (None, '-QUIT-'):
            break
        
    window.close()

if __name__ == '__main__':
        print("Starting program...")
        main(refresh_rate=5)