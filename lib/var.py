import time
import configparser

current_state = "START_TURN"
turn_completed = 0
n = 0
start_time = time.time()
time_elapsed = 0

b4_last_loc = 0
b4_last_pos = [0, 0]
b4_trigger = 0
last_loc = 0
last_pos = [0, 0]

# to do
early_retreats = None
emu = None
strat = None
coord = []

dc_n = 0
zone_info = [0, 0, 0]
zone_scores = [0, 0, 0]

debug_state = 0

locConfig = configparser.ConfigParser()
locConfig.read("locations.ini")

game_path = "D:\\SteamLibrary\\steamapps\\common\\MARVEL SNAP\\SNAP.exe"

child = 0

initial_xp = 0
