import time
import random
from lib.image_processing import *
from lib.utils import *
import lib.var as var
import pyautogui


def drag():
    turn_num = var.turn_completed + 1
    if turn_num <= 3:
        # if turn_num == 3: add later
        var.zone_info = get_zone_info()
        print(f"zone_info: {var.zone_info}")
    if turn_num >= 1:
        # if turn_num >= 3: add later
        var.zone_scores = get_losing_zones()
        print(f"zone_scores: {var.zone_scores}")
    # max_search = turn_num + 1 if turn_num <= 2 else 5
    # max_search = 2 if turn_num <= 2 else 5 add later
    max_search = 5
    for _ in range(max_search):
        dest = None
        button_position = locate_color_on_screen(
            0x2548FF, region=region_raw_convert(var.coord["REGION_DRAG_CARDS_RAW"])
        )
        if button_position is not None:
            dest = strat_5(button_position)
            swipe(
                button_position[0] + 20,
                button_position[1] + 20,
                var.coord["DRAG_TO"][dest],
                var.coord["DRAG_TO"][3],
                50,
            )
            tap(var.coord["IDLE_MOUSE_POSITION"])
            # var.b4_last_loc
            var.last_loc = dest
            var.last_pos = button_position
            time.sleep(0.1)
        else:
            break
    tap_away(var.coord["END_TURN_BUTTON"])
    var.last_pos = (0, 0)
    var.zone_scores = [0, 0, 0]
    var.turn_completed += 1


# added extra last position history
def drag2():
    turn_num = var.turn_completed + 1
    if turn_num <= 3:
        # if turn_num == 3: add later
        var.zone_info = get_zone_info()
        print(f"zone_info: {var.zone_info}")
    if turn_num >= 1:
        # if turn_num >= 3: add later
        var.zone_scores = get_losing_zones()
        print(f"zone_scores: {var.zone_scores}")
    # max_search = turn_num + 1 if turn_num <= 2 else 5
    # max_search = 2 if turn_num <= 2 else 5 add later
    max_search = 5
    for _ in range(max_search):
        dest = None
        button_position = locate_color_on_screen(
            0x2548FF, region=region_raw_convert(var.coord["REGION_DRAG_CARDS_RAW"])
        )
        if button_position is not None:
            match var.strat:
                case "v4":
                    dest = strat_4(button_position)
                case "v6":
                    dest = strat_6(button_position)
                case _:
                    dest = 0
            # dest = strat_6(button_position)
            swipe(
                button_position[0] + 20,
                button_position[1] + 20,
                var.coord["DRAG_TO"][dest],
                var.coord["DRAG_TO"][3],
                50,
            )
            tap(var.coord["IDLE_MOUSE_POSITION"])
            var.b4_last_loc = var.last_loc
            var.b4_last_pos = var.last_pos
            var.last_loc = dest
            var.last_pos = button_position
            time.sleep(0.1)
        else:
            break
    tap_away(var.coord["END_TURN_BUTTON"])
    var.last_pos = (0, 0)
    var.zone_scores = [0, 0, 0]
    var.turn_completed += 1


def strat_3(button_position):
    # turn_completed updates after dragging
    turn_num = var.turn_completed + 1
    if turn_num == 1:
        return 1
    elif turn_num == 2:
        return 2
    elif turn_num == 3:
        return handle_best_zone_or_random(button_position, 2)
    else:
        return handle_best_zone_or_random(button_position, 3)


def strat_4(button_position):
    turn_num = var.turn_completed + 1
    if turn_num == 1:
        return 1
    elif turn_num == 2:
        return 2
    elif turn_num == 3:
        return handle_best_zone_or_random3(button_position, 3)
    else:
        return handle_best_zone_or_random3(button_position, 3)


# temporary
def strat_5(button_position):
    return handle_best_zone_or_random2(button_position, 3)


def strat_6(button_position):
    return handle_best_zone_or_random3(button_position, 3)


# only run once
def get_losing_zones():
    score_pos = [(145, 381), (256, 373), (368, 378)]
    score_list = [0, 0, 0]
    [pyautogui.pixel(point[0], point[1]) for point in score_pos]
    for index, point in enumerate(score_pos):
        # find grey
        if pyautogui.pixelMatchesColor(
            point[0], point[1], (0x59, 0x43, 0x3E), tolerance=10
        ):
            score_list[index] = 1
    return score_list


def get_best_zone2(selection=[0, 1, 2]):
    # select elements from zone_info based on the indices in selection
    selected_list = [var.zone_info[i] for i in selection]
    # find the index of the maximum value in the selected list
    max_value = max(selected_list)
    max_indexes = [i for i, j in enumerate(selected_list) if j == max_value]
    losing_zones = var.zone_scores
    max_indexes_in_complete_list = [selection[i] for i in max_indexes]
    weighted_max_indexes = []
    for index in max_indexes_in_complete_list:
        if losing_zones[index] == 1:
            weighted_max_indexes.append(index)
    # weighted_max_indexes = filter max indexes then losing indexes
    if weighted_max_indexes != []:
        max_index_in_complete_list = random.choice(weighted_max_indexes)
    else:
        max_index_in_complete_list = random.choice(max_indexes)
    return max_index_in_complete_list


def handle_best_zone_or_random(button_position, x):
    if button_position[0] == var.last_pos[0] and button_position[1] == var.last_pos[1]:
        banned_pos = var.last_loc
        # tends to go zone 0
        dest = (
            random_int_exclude(banned_pos, list(range(x)))
            if banned_pos < x
            else get_best_zone(range(x))
        )
    else:
        dest = get_best_zone(range(x))
    return dest


def handle_best_zone_or_random2(button_position, x):
    if button_position[0] == var.last_pos[0] and button_position[1] == var.last_pos[1]:
        banned_pos = var.last_loc
        # tends to go zone 0
        dest = (
            random_int_exclude(banned_pos, list(range(x)))
            if banned_pos < x
            else get_best_zone2(range(x))
        )
    else:
        dest = get_best_zone2(range(x))
    return dest


# 2 histories
def handle_best_zone_or_random3(button_position, x):
    if button_position[0] == var.last_pos[0] and button_position[1] == var.last_pos[1]:
        var.b4_trigger += 1
        if var.b4_trigger == 1:
            banned_pos = var.last_loc
            # tends to go zone 0
            dest = (
                random_int_exclude(banned_pos, list(range(x)))
                if banned_pos < x
                else get_best_zone2(range(x))
            )
        elif var.b4_trigger == 2:
            result = [0, 1, 2]
            result = [x for x in result if x != var.b4_last_loc and x != var.last_loc]
            dest = result[0]
        else:
            var.b4_trigger = 0
            dest = get_best_zone2(range(x))
    else:
        var.b4_trigger = 0
        dest = get_best_zone2(range(x))
    return dest


def get_best_zone(selection=[0, 1, 2]):
    # select elements from zone_info based on the indices in selection
    selected_list = [var.zone_info[i] for i in selection]
    # find the index of the maximum value in the selected list
    max_value = max(selected_list)
    max_indexes = [i for i, j in enumerate(selected_list) if j == max_value]
    max_rand_index_in_selected_list = random.choice(max_indexes)
    # find the original index of the selected list
    max_index_in_complete_list = selection[max_rand_index_in_selected_list]
    return max_index_in_complete_list


def strat_2(button_position):
    # turnCompleted updates after dragging
    turn_num = var.turn_completed + 1
    if turn_num == 1:
        return 1
    elif turn_num == 2:
        return 2
    elif turn_num == 3:
        return tmp(button_position, 2)
    else:
        return tmp(button_position, 3)


# purely random
def strat_1(button_position):
    return tmp(button_position, 3)


def tmp(button_position, x):
    if button_position[0] == var.last_pos[0] and button_position[1] == var.last_pos[1]:
        banned_pos = var.last_loc
        dest = random_int_exclude(banned_pos, list(range(x))) if banned_pos < x else 0
    else:
        dest = random.randint(0, x - 1)
    return dest


# run exactly once per game
def get_zone_info():
    if var.emu:
        return [0, 0, 0]
    reg = (97, 297, 400, 335)
    sep_1, sep_2 = 200, 300
    zone_info = [0, 0, 0]
    loc_list = os.listdir(".\\images\\locations")
    for name in loc_list:
        point = location_check(name, confidence=0.85, region=reg)
        if point:
            zone = 0 if point.x <= sep_1 else 1 if point.x <= sep_2 else 2
            print(f"Found {name} at zone: {zone}")
            name_minus_ext = name.split(".")[0]
            loc_score = (
                var.locConfig["scores"][name_minus_ext]
                if var.locConfig.has_option("scores", name_minus_ext)
                else 0
            )
            if zone_info[zone] != 0:
                print(f"Messed up! zone={zone_info}. Ignored all results.")
                zone_info = [0, 0, 0]
                return zone_info
            zone_info[zone] = int(loc_score)
    return zone_info
