import os
from pyautogui import *
import win32gui
import win32ui
from ctypes import windll
import time
import cv2
import numpy as np
from matplotlib import pyplot as plt


script_dir = os.path.dirname(os.path.abspath(__file__))

region = (0, 0, 480, 718)  # inaccurate


def image_check(
        str,
        confidence=0.95,
        region=region,
        grayscale=True,
        emulator=False):
    if (emulator):
        image_path = os.path.join(script_dir, '..', 'images_emulator')
    else:
        image_path = os.path.join(script_dir, '..', 'images')
    image_pos = locateCenterOnScreen(
        image_path + '/' + str + '.png',
        confidence=confidence,
        grayscale=grayscale,
        region=region)
    return image_pos


def location_check(
        name,
        confidence=0.9,
        region=region,
        grayscale=True,
        emulator=False):
    if (emulator):
        image_path = os.path.join(
            script_dir, '..', 'images_emulator\\locations')
    else:
        image_path = os.path.join(script_dir, '..', 'images\\locations')
    image_pos = locateCenterOnScreen(
        image_path + '/' + name,
        confidence=confidence,
        grayscale=grayscale,
        region=region)
    return image_pos


def locate_color_on_screen(rgbHex, region=region):
    color = hex_2_dec(rgbHex)
    image = screenshot(region=region)
    # print(image.width,image.height)
    step = 2  # skipping pixels
    for x in range(0, image.width, step):
        for y in range(0, image.height, step):
            # Get the RGB color of the pixel at (x, y)
            pixel_color = image.getpixel((x, y))
            if pixel_color == color:
                # add top left corner coord, inaccurate
                x1, y1 = x + region[0], y + region[1]
                print(f"Dragging card: ({x1}, {y1})")
                return (x1, y1)

    return None


def hex_2_dec(hex_color):
    hex_color = 0x2548ff
    red = (hex_color >> 16) & 0xff
    green = (hex_color >> 8) & 0xff
    blue = hex_color & 0xff
    return (red, green, blue)

def get_image_from_pname(pname):
    hwnd = win32gui.FindWindow(None, pname)
    # hwnd= win32gui.FindWindowEx(hwnd0, None, None, None)
    # Change the line below depending on whether you want the whole window
    # or just the client area. 
    left, top, right, bot = win32gui.GetClientRect(hwnd)
    # left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area. 
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)

    print(result)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    # 
    img_arr = np.frombuffer(bmpstr, dtype=np.uint8).reshape(height, width, 4)
    return img_arr


def get_pos(pname,tname,region,grayscale=False,confidence=0.1,method=cv2.TM_SQDIFF_NORMED):
    img1 = get_image_from_pname(pname)
    img2 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY) if grayscale else cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
    template=cv2.imread('images_emulator/'+tname+'.png',cv2.IMREAD_GRAYSCALE) if grayscale else cv2.imread('images_emulator/'+tname+'.png')
    if region==-1:
        y1,x1=0,0
        height=img1.shape[0]
        width=img1.shape[1]
    else:
        y1,x1,height,width = region[1],region[0],region[3],region[2] # 632,266,83,131
    cropped=img2[y1:y1+height,x1:x1+width] if grayscale else img2[y1:y1+height,x1:x1+width,:]
    print("checking tname",tname,"region:",region,"src dim:",cropped.shape,"des:",template.shape)

    res = cv2.matchTemplate(cropped,template,method)

    min_val, _, min_loc, _ = cv2.minMaxLoc(res)

    print(min_val, min_loc)
    (h,w)=template.shape[:2]

    if (min_val<confidence):
        # return (min_loc[0]+h,min_loc[1]+w)
        return (min_loc[0]+x1+h//2,min_loc[1]+y1+w//2)
    return None

def bg_image_check(
        tname,
        region,
        confidence=0.95,
        grayscale=True,
        emulator=True):
    return get_pos("LDPlayer",tname,region,confidence=confidence,grayscale=grayscale)
    


