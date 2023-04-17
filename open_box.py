import time
from pyautogui import *
import win32api
from win32con import *
import win32gui

process_name = 'SNAP'
hwnd = win32gui.FindWindow(None, process_name)
if not hwnd:
    win32gui.MessageBox(
        None,
        f'Process not found: "{process_name}.exe"',
        "Oh, Snap!",
        0)
    raise KeyboardInterrupt
win32gui.MessageBox(None, "Move mouse to box position, you have 3 seconds.", "", 0)
win32gui.SetForegroundWindow(hwnd)
width, height = 405, 720
win32gui.MoveWindow(hwnd, 0, 0, width, height, True)

time.sleep(3)
x,y=position()
while True:
    click(x,y)
    time.sleep(0.1)
    while True:   
        p = locateCenterOnScreen('./bp/claim.png',confidence=0.9,region=(0,0,360,640))
        if p is not None:
            print("checking image")
            click(248,588)
            time.sleep(0.3)
            break
        time.sleep(0.3)
    moveTo(x,y)
    time.sleep(0.1)
    win32api.mouse_event(MOUSEEVENTF_WHEEL, x,y, 120, 0)
    time.sleep(0.1)
