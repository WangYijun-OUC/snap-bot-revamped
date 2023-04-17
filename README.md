<h1 align="center">
  Snap Bot Revamped
</h1>

This project performs play automation of Marvel Snap using screencapture and mouseclick functions in python libraries (mainly opencv-python, pyautogui), analyzing the screenshot, and perform actions. This is a revamped version of my previous [project](https://github.com/methreals/snapBOT), featuring improved play card strategies, XP efficiency and a user friendly ui. 

## How to use:
1. Download the [installer](https://github.com/methreals/snap-bot-revamped/releases/download/release/snap-bot-revamped_v.1.0.exe) from [release page](https://github.com/methreals/snap-bot-revamped/releases/tag/release)

2. Launch steam version of marvel snap
    - window mode, language: English, quality: Low

3. Eun the exe file, no extra libraries needed

4. If you prefer to run from source code, it requires Python 3.10 or above 
    - pip install pillow opencv-python pywin32 pyautogui
    - run *gui_main.py*
    - you can use *open_box.py*: A simple tool to open season caches automatically.

The program needs to be on foreground window and you can't use the computer while running. To run on background, you can use a virtual machine. I highly recommend VMWare Workstation pro if you can afford it.

> Here's my own setting of *VMWare Workstation pro 17.0.0 build-20800274* (probably overkill):  <br> 
Windows 10 (latest update), memory: 4GB, processor: 1 core: 4, graphics: 8GB memory, accelerated 3D graphics

## Screenshots:
![Screenshot of the program](/res/programSample2.PNG)

## Features: 

### XP Farm mode: 
retreat as soon as turn 3 is finished, bring lots of good 1-3 drops

### Full game mode:
booster farm, do missions, climb ranks with correct decks

### Emulator mode:
bot working outside android emulator (running snap)

discontinued due to ban reports

### Strategy:
***v4:*** turn 1: middle, turn 2: right, turn 3+: best locations

***v6:*** best locations (recommended)

<br>

***Play prioity:*** best location based on scores in *locations.ini* **->** random losing/draw location **->** location according to self correction rule (explanation below)

***Self correction rule:*** If a card is dragged to a prohibitive location, it would drag to a random location of the rest 2. If it goes to a prohibitive location again, it would drag to the last available location. If all three locations are unavailable to play on (e.g. triple spidermen), it would stop trying after 5 fails and end turn.

***Tracking of stats:*** current season pass level, season pass level per day, XP per match, reconnected times, etc

***Auto relaunch game*** when getting stuck for more than 3 minutes

***Randomized clicks*** to avoid detection.

***Right ctrl*** hotkey to quickly close the program while running

## Update the tool:
***update images:***
check *./images/* folder and replace the outdated images 
- take screenshot and crop the image parts using clipping tool (Win+Shift+S)
> Different machines or virtual machines can have different graphical render methods so you may have to update the images for your own PC specifically. 

***modify locations scores:*** *locations.ini*

## 
This program does not access game memory or modify files but please be clear that using it can result in account suspension when detected or reported by other players.

## Credits:
* strategies, battlepass XP from 7F and 可可丁 
* used small section of code from AdriaGual's [Marvel Snap Bot](https://github.com/AdriaGual/marvel-snap-bot)

## License:

GNU General Public License v3.0
