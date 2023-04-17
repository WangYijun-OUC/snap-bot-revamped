from lib.image_processing import *
from lib.utils import *
import lib.coordinates
import time
import random
import lib.strategy as strategy
import lib.var as var
import lib.timer_related as timer_related
import gui
from lib.image_search import *

# self.turnCompleted = 0
# self.current_state = 'START_TURN'
# self.early_retreats = early_retreats
# self.emu = emu
# self.n = 0
# self.start_time = time.time()
# self.time_elapsed = 0

# self.lastLoc = 0
# self.lastPos = [0,0]
# if (emu):
#     self.region = (0, 0, 403, 718)
#     self.coord = lib.coord.emu
# else:
#     self.region = (10, 32, 490 - 10, 671 - 32)
#     self.coord = lib.coord.PC
# return


def play_cards_transition():
    # start turn check
    sleepTime = 0.2
    button_position = imgSearch.check_turn_start()
    if button_position is not None:
        time.sleep(sleepTime)
        return True
    button_position2 = imgSearch.check_turn_start_2()
    if button_position2 is not None:
        time.sleep(sleepTime)
        return True
    return False


def battle_transition():
    # play cards
    strategy.drag2()

    print(f"turnCompleted: {var.turn_completed}")
    time.sleep(0.5)
    return True


def retreat_transition():
    # check if im losing , or after 3rd turn
    if var.early_retreats and var.turn_completed >= 3:
        button_position = imgSearch.check_3rd_turn()
        if button_position is not None or var.turn_completed >= 4:
            tap(var.coord["RETREAT_BUTTON_1"])
            time.sleep(0.4)
            tap(var.coord["RETREAT_BUTTON_2"])
            time.sleep(1.5)
            return True
    return False


def snap_transition():
    # true if I'm winning lanes. skip
    return False


def collect_rewards_transition():
    # check collect button
    button_position = imgSearch.check_collect_button()
    if button_position is not None:
        tap_away(button_position)
        return True
    return False


def start_turn_transition():
    # check start turn button
    return play_cards_transition()


def next_transition():
    # check next button
    button_position = imgSearch.check_next_button()
    if button_position is not None:
        tap(button_position)
        return True
    # avoid getting stuck
    collect_rewards_transition()
    return False


def main_menu_transition():
    # check play button
    button_position = imgSearch.check_mission_text()
    if button_position is not None:
        var.turn_completed = 0
        var.n += 1
        var.zone_info = [0, 0, 0]
        timer_related.TimerManager.record_timer()
        stat_calc()

        for _ in range(4):
            tap(var.coord["PLAY_BUTTON"])
            time.sleep(1)
        # time.sleep(1)
        return True
    return False


def start_game_transition():
    # ?
    return True


def stat_calc():
    var.time_elapsed = time.time() - var.start_time
    hr_elapsed = var.time_elapsed / 3600
    n_hr = var.n / hr_elapsed
    levelinfo = calc_level()
    level = levelinfo[0]
    xp_gained = levelinfo[1] - var.initial_xp
    xp_n = xp_gained / var.n
    lv_d = xp_n * n_hr * 24 / 1000
    str = "n: %u, %.1fh, %u/h, dc: %u\n" % (var.n, hr_elapsed, n_hr, var.dc_n)
    str += "LV %u, %.1fXP/n, %.1fLV/d" % (level, xp_n, lv_d)

    # print(str)
    if not var.emu:
        gui.my_GUI.lblVar.set(value=str)
