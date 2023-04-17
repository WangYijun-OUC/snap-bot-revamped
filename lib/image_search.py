from lib.image_processing import *
from lib.utils import *
import lib.var as var


class imgSearch:
    def check_mission_text():
        return image_check(
            'mission',
            emulator=var.emu,
            region=region_raw_convert(
                var.coord['REGION_MISSION_RAW']))

    def check_next_button():
        return image_check('next', emulator=var.emu, region=region_raw_convert(
            var.coord['REGION_LOWER_RIGHT_RAW']))

    def check_collect_button():
        return image_check(
            'collectRewards',
            confidence=0.9,
            emulator=var.emu,
            region=region_raw_convert(
                var.coord['REGION_LOWER_RIGHT_RAW']))

    def check_retreat_button():
        return image_check('retreat', confidence=0.95, emulator=var.emu)

    def check_turn_start():
        return image_check(
            'startTurn',
            confidence=0.97,
            grayscale=False,
            emulator=var.emu,
            region=region_raw_convert(
                var.coord['REGION_LOWER_RIGHT_RAW']))

    def check_turn_start_2():
        return image_check(
            'startTurn2',
            confidence=0.97,
            grayscale=False,
            emulator=var.emu,
            region=region_raw_convert(
                var.coord['REGION_LOWER_RIGHT_RAW']))

    def check_3rd_turn():
        return image_check(
            'playing36_1',
            confidence=0.9,
            grayscale=False,
            emulator=var.emu,
            region=region_raw_convert(
                var.coord['REGION_LOWER_RIGHT_RAW']))
