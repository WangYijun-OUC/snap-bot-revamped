import time


class TimerManager:
    DC_TIME = 3
    DC_LOCK = 4
    startTime = 0
    lastDC = 0
    timeSinceLastDC = 0
    timeInGame = 0
    oldTimeInGame = 0
    periodicTimer = 0

    def update():
        TimerManager.startTime = time.time()
        TimerManager.lastDC = TimerManager.startTime
        TimerManager.timeSinceLastDC = TimerManager.startTime
        TimerManager.timeInGame = TimerManager.startTime
        TimerManager.oldTimeInGame = TimerManager.startTime
        TimerManager.periodicTimer = TimerManager.startTime

    def time_exceeds_by_min(t1, t2, min):
        return (t1 - t2) / 60 > min

    def record_timer():
        TimerManager.oldTimeInGame = time.time()

    def update_TIG():
        TimerManager.timeInGame = time.time()

    def update_dc_time():
        TimerManager.timeSinceLastDC = time.time() - TimerManager.lastDC

    def update_last_dc():
        TimerManager.lastDC = time.time()

    def should_reconnect():
        TimerManager.update_TIG()
        TimerManager.update_dc_time()
        if (TimerManager.time_exceeds_by_min(TimerManager.timeInGame, TimerManager.oldTimeInGame,
                                             TimerManager.DC_TIME) and TimerManager.timeSinceLastDC > TimerManager.DC_LOCK * 60):
            TimerManager.update_last_dc()
            return True
        return False

    def periodic_check(sec):
        if time.time() - TimerManager.periodicTimer > sec:
            TimerManager.periodicTimer = time.time()
            return True
        return False

    def debug():
        print(f"tig:{(int)(TimerManager.timeInGame)},otig={(int)(TimerManager.oldTimeInGame)},\
              tebm={TimerManager.time_exceeds_by_min(TimerManager.timeInGame, TimerManager.oldTimeInGame, TimerManager.DC_TIME)},dcT={TimerManager.timeSinceLastDC}")

    def get_time_stat_gui():
        tmp_str= "tig = %d" % (TimerManager.timeInGame-TimerManager.oldTimeInGame)
        # print(tmp_str)
        return tmp_str