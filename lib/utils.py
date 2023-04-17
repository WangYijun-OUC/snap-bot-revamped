import pyautogui
import time
import random
import lib.coordinates
import signal
import os
from pynput import keyboard
import subprocess
import win32gui
import lib.var as var
import configparser
import json
import win32api
import win32con


# duration in ms


def swipe(x1, y1, x2, y2, duration):
    maxRandNum = 5
    x1 = x1 + random.randint(0, maxRandNum)
    x2 = x2 + random.randint(0, maxRandNum)
    y1 = y1 + random.randint(0, maxRandNum)
    y2 = y2 + random.randint(0, maxRandNum)
    pyautogui.mouseDown(x1, y1)
    pyautogui.moveTo(x2, y2, duration=duration / 1000)
    pyautogui.mouseUp()
    time.sleep(0.08)
    pyautogui.moveTo(
        lib.coordinates.IDLE_MOUSE_POSITION[0], lib.coordinates.IDLE_MOUSE_POSITION[1]
    )
    pyautogui.click()


def tap(pos):
    maxRandNum = 5
    x, y = pos[0] + random.randint(0, maxRandNum), pos[1] + random.randint(
        0, maxRandNum
    )
    pyautogui.click(x, y)


def tap_away(pos):
    tap(pos)
    pyautogui.moveTo(
        lib.coordinates.IDLE_MOUSE_POSITION[0], lib.coordinates.IDLE_MOUSE_POSITION[1]
    )


def tap_away_tap(pos):
    tap(pos)
    tap(lib.coordinates.IDLE_MOUSE_POSITION)


def region_raw_convert(raw_region):
    return (
        raw_region[0],
        raw_region[1],
        raw_region[2] - raw_region[0],
        raw_region[3] - raw_region[1],
    )


def random_int_exclude(a, options):
    options.remove(a)
    return random.choice(options)


def on_press(key):
    try:
        if key == keyboard.Key.ctrl_r:
            print("Stopped.")
            os.kill(os.getpid(), signal.SIGINT)
    except Exception as e:
        print("Error: {}".format(e))


def startProcess(processName):
    pro = '"{}"'.format(processName)
    subprocess.Popen(pro, close_fds=True)


def killProcess(processName):
    pro = "%s%s.exe" % ("C:\\windows\\system32\\taskkill /F /IM ", processName)
    subprocess.Popen(pro, close_fds=True)
    # os.system('%s%s' % ("C:\windows\system32\\taskkill /F /IM ",processName))


def reconnect():
    # only steam atm
    print("Reconnecting")
    process_name = "SNAP"
    killProcess(process_name)
    time.sleep(2)
    hwnd = win32gui.FindWindow(None, process_name)
    while hwnd:
        print("Process still open.")
        killProcess(process_name)
        time.sleep(2)
        hwnd = win32gui.FindWindow(None, process_name)
    fullpath = var.game_path
    startProcess(fullpath)

    time.sleep(10)

    print("Reconnected")
    var.dc_n += 1


def launchGame():
    process_name = "SNAP"
    hwnd = win32gui.FindWindow(None, process_name)
    if not hwnd:
        fullpath = var.game_path
        startProcess(fullpath)
    else:
        win32gui.MessageBox(None, "Game is already opened.", "Error", 0)


def calc_level():
    appdata_path = os.getenv("APPDATA")
    path = os.path.join(
        appdata_path,
        "..",
        "LocalLow",
        "Second Dinner",
        "SNAP",
        "Standalone",
        "States",
        "nvprod",
        "BattlePassState.json",
    )

    try:
        with open(path) as f:
            next(f)
            data = f.read()
            data = "{" + data
            data = json.loads(data)

            if (
                "ServerState" in data
                and "BattlePass" in data["ServerState"]
                and "Level" in data["ServerState"]["BattlePass"]
            ):
                level = int(data["ServerState"]["BattlePass"]["Level"])
            else:
                print("Required level keys not found in the JSON")
                level = 0

            if (
                "ServerState" in data
                and "BattlePass" in data["ServerState"]
                and "Xp" in data["ServerState"]["BattlePass"]
            ):
                xp = int(data["ServerState"]["BattlePass"]["Xp"])
            else:
                xp = 0
                print("Required Xp keys not found in the JSON")
            xp_total = level * 1000 + xp
            return level, xp_total
    except:
        print("An error occurred while opening the file.")
        return 0, 0


def control_click(x, y):
    pos = win32api.MAKELONG(x, y)
    win32gui.SendMessage(var.child, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, pos)
    time.sleep(0.1)
    win32gui.SendMessage(var.child, win32con.WM_LBUTTONUP, None, pos)


def control_tap(pos):
    maxRandNum = 5
    x, y = pos[0] + random.randint(0, maxRandNum), pos[1] + random.randint(
        0, maxRandNum
    )
    control_click(x, y)


def control_tap_away(pos):
    control_tap(pos)


def control_tap_away_tap(pos):
    control_tap(pos)
