"""
Main GUI

"""

# from tkinter import *
import tkinter as tk
import threading
import time
from tkinter import ttk, filedialog
import win32gui
import lib.var as var
import lib.coordinates as coordinates
import lib.bot_state as bot_state
import configparser
from pynput import keyboard
import lib.utils as utils
from PIL import Image, ImageTk
import lib.timer_related as timer_related


class my_GUI:
    running = False
    mode = None
    env = None
    strat = None
    bot = bot_state.BotState()
    root = tk.Tk()
    config = configparser.ConfigParser()
    lblStat = 0
    lblVar = tk.StringVar()
    t = timer_related.TimerManager()

    def __init__(self):
        self.first_time = True
        self.load_config_to_var()
        # style = ttk.Style()
        # style.theme_use('clam')
        my_GUI.root.title("")
        my_GUI.root.resizable(width=False, height=False)
        self.mainframe = ttk.Frame(my_GUI.root, padding=19)

        self.subframe1 = ttk.Frame(self.mainframe)

        self.subframe2 = ttk.Frame(self.mainframe)

        self.subframe3 = ttk.Frame(self.mainframe)
        self.subframe4 = ttk.Frame(self.mainframe)

        self.game_path = tk.StringVar(value=var.game_path)
        self.game_path_text = ttk.Entry(
            self.subframe3, textvariable=self.game_path, width=23
        )
        self.game_path_text.configure(state=tk.DISABLED)

        self.path_button = ttk.Button(
            self.subframe3, text="...", width=5, command=self.handle_file
        )

        my_GUI.mode = tk.StringVar()
        self.combobox = ttk.Combobox(
            self.subframe2, textvariable=my_GUI.mode, values=["Full Game", "XP Farm"]
        )
        self.combobox.state(["readonly"])
        self.combobox.current(1) if var.early_retreats else self.combobox.current(0)

        my_GUI.env = tk.StringVar()
        self.combobox2 = ttk.Combobox(
            self.subframe2,
            textvariable=my_GUI.env,
            values=["Steam (Windows)", "LDPlayer4"],
        )
        self.combobox2.state(["readonly"])
        self.combobox2.current(1) if var.emu else self.combobox2.current(0)

        my_GUI.strat = tk.StringVar()
        self.combobox3 = ttk.Combobox(
            self.subframe2,
            textvariable=my_GUI.strat,
            values=["v4", "v6"],
        )
        self.combobox3.state(["readonly"])
        self.combobox3.current(1)

        self.img = Image.open("./res/pause.png")
        self.img = self.img.resize((75, 75))
        self.photo = ImageTk.PhotoImage(self.img)
        self.img2 = Image.open("./res/run.png")
        self.img2 = self.img2.resize((75, 75))
        self.photo2 = ImageTk.PhotoImage(self.img2)

        self.start_button = ttk.Button(
            self.subframe1, command=self.toggle, image=self.photo2
        )

        self.checkbutton_strvar = tk.StringVar()
        self.check_button = ttk.Checkbutton(
            self.subframe4,
            text="debug",
            variable=self.checkbutton_strvar,
            command=self.checkbutton_cmd,
        )

        self.help_button = ttk.Button(
            self.subframe4, text="Help", width=5, command=self.show_help
        )

        self.launch_process_button = ttk.Button(
            self.subframe4, text="Launch SNAP", command=utils.launchGame
        )

        self.style = ttk.Style()
        self.style.configure("lblStat.TLabel", foreground="blue", font="Helvetica 8")
        my_GUI.tigvar = tk.StringVar(
            value=str(timer_related.TimerManager.get_time_stat_gui())
        )
        my_GUI.tiglbl = ttk.Label(
            self.subframe4, textvariable=my_GUI.tigvar, style="lblStat.TLabel"
        )
        # my_GUI.tigvar.set(value=str(timer_related.TimerManager.get_time_stat_gui()))
        # self.tiglbl.configure(text='0')

        my_GUI.lblVar = tk.StringVar()

        # my_GUI.lblStat = ttk.Label(
        #     self.subframe4,
        #     textvariable=my_GUI.lblVar,
        #     width=28,
        #     style="lblStat.TLabel",anchor='center')
        my_GUI.lblStat = tk.Message(
            self.subframe4,
            textvariable=my_GUI.lblVar,
            width=180,
            fg="blue",
            anchor="center",
        )
        self.lbl1 = ttk.Label(self.subframe2, text="Mode")
        self.lbl2 = ttk.Label(self.subframe2, text="Platform")
        self.lbl3 = ttk.Label(self.subframe2, text="Strategy")
        level = (utils.calc_level())[0]
        my_GUI.lblVar.set(value=f"LV {level}\n")
        # my_GUI.lblVar.set(value=f"n: 111, LV 111, 11.1h, 111/h, dc: 1")
        # self.lbl3 = Label(self.mainframe,text="")

        self.geo_manager()

        # width, height, screen_width, screen_height = 350, 160, 1920, 1080
        # x = (screen_width/2) - (width/2)
        # y = (screen_height/2) - (height/2) - 50
        # gui.root.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def toggle(self):
        if my_GUI.running:
            print("Script stopped.")
            my_GUI.running = False
            self.start_button.config(text="Start", image=self.photo2)
        else:
            if self.init_setting():
                print("Script started.")
                my_GUI.running = True
                var.initial_xp = (utils.calc_level())[1]
                self.start_button.config(text="Stop", image=self.photo)
                thread = threading.Thread(target=self.action)
                thread.start()

    def run(self):
        my_GUI.root.mainloop()

    def show_help(self):
        help_text = "How to use: \nClick 'PLAY' button manually then start the script.\nDisplay scale 100% \nEnglish, Low Quality \nIf using LDPlayer4: \nResolution = 720x1280 collapsed sidebar\nYou can press stop or exit using hotkey RCtrl.\nHow to read status:\nn = number of games, \nhow many hours passed, \nand games per hour\nhttps://github.com/methreals/snapBOT"
        # tkinter.messagebox.showinfo("Help", help_text)
        win32gui.MessageBox(None, help_text, "Help", 0)

    def init_setting(self):
        # config writing
        print("init_setting start")
        my_GUI.config.set("config", "RETREAT", str(self.combobox.current()))
        my_GUI.config.set("config", "EMULATOR", str(self.combobox2.current()))
        my_GUI.config.set("config", "strat", str(self.combobox3.current()))
        with open("config.ini", "w") as f:
            my_GUI.config.write(f)

        var.early_retreats = True if my_GUI.mode.get() == "XP Farm" else False
        var.emu = True if my_GUI.env.get() == "LDPlayer" else False
        var.coord = (
            coordinates.emu if my_GUI.env.get() == "LDPlayer" else coordinates.PC
        )
        var.strat = my_GUI.strat.get()

        process_name = "SNAP" if not var.emu else "LDPlayer"
        process_exe = "SNAP" if process_name == "SNAP" else "dnplayer"
        hwnd = win32gui.FindWindow(None, process_name)
        if not hwnd:
            win32gui.MessageBox(
                None, f'Process not found: "{process_exe}.exe"', "Oh, Snap!", 0
            )
            return False
        if self.first_time:
            win32gui.MessageBox(None, "Click 'PLAY' button.", "", 0)
            self.first_time = False
        win32gui.SetForegroundWindow(hwnd)
        width, height = 405, 720
        win32gui.MoveWindow(hwnd, 0, 0, width, height, True)
        var.turn_completed = 0
        print("init_setting finsihed")
        return True

    def geo_manager(self):
        self.mainframe.grid(
            column=0, row=0, columnspan=2, sticky=(tk.N, tk.W, tk.E, tk.S)
        )
        self.subframe1.grid(row=0, column=0, rowspan=3)
        self.subframe2.grid(row=3, column=0, rowspan=2)
        self.subframe3.grid(row=5, column=0, rowspan=1)
        self.subframe4.grid(row=6, column=0, rowspan=2)

        self.start_button.grid(
            row=0, column=0, rowspan=3, columnspan=3, padx=15, pady=10
        )

        self.combobox.grid(row=3, column=1, columnspan=2, pady=2, sticky="w")
        self.lbl1.grid(row=3, column=0, sticky="w")
        self.combobox2.grid(row=4, column=1, columnspan=2, pady=2, sticky="w")
        self.lbl2.grid(row=4, column=0, sticky="w")
        self.combobox3.grid(row=5, column=1, columnspan=2, pady=2, sticky="w")
        self.lbl3.grid(row=5, column=0, sticky="w")

        self.game_path_text.grid(row=0, column=0, columnspan=1, pady=4, sticky="ew")
        self.path_button.grid(row=0, column=1)

        my_GUI.lblStat.grid(row=0, column=0, columnspan=6, pady=0, sticky=("ew"))

        # self.check_button.grid(row=1, column=0, sticky='')
        my_GUI.tiglbl.grid(row=1, column=0)
        # self.help_button.grid(row=1, column=1, padx=0, pady=3, sticky='e')
        self.launch_process_button.grid(row=1, column=2, sticky="ew", padx=5)

    def load_config_to_var(self):
        my_GUI.config.read("config.ini")
        var.early_retreats = my_GUI.config.getboolean("config", "RETREAT")
        var.emu = my_GUI.config.getboolean("config", "EMULATOR")
        var.strat = my_GUI.config.get("config", "strat").replace("\n", "")
        var.game_path = my_GUI.config.get("config", "gamepath").replace("\n", "")

    def handle_file(self):
        file = filedialog.askopenfilename()
        self.game_path_text.configure(state=tk.NORMAL)
        self.game_path.set(value=file)
        self.game_path_text.configure(state=tk.DISABLED)
        my_GUI.config.set("config", "gamepath", file)
        with open("config.ini", "w") as f:
            my_GUI.config.write(f)
        var.game_path = file

    def checkbutton_cmd(self):
        var.debug_state = int(self.checkbutton_strvar.get())

    def action(self):
        # bot = botState()
        with keyboard.Listener(on_press=utils.on_press) as listener:
            # initialize timeVar and check state
            time.sleep(2)
            timer_related.TimerManager.update()
            my_GUI.bot.update_state()

            while my_GUI.running:
                if timer_related.TimerManager.periodic_check(10):
                    my_GUI.bot.update_state()

                if timer_related.TimerManager.periodic_check(5):
                    # my_GUI.bot.print_state()
                    if timer_related.TimerManager.should_reconnect():
                        utils.reconnect()
                        time.sleep(5)
                        self.init_setting()
                        var.current_state = "NEXT"

                    my_GUI.tigvar.set(
                        value=str(timer_related.TimerManager.get_time_stat_gui())
                    )

                    # timeVar.timeVar.debug()
                # if timer_related.TimerManager.periodic_check(1):

                if var.debug_state:
                    if timer_related.TimerManager.periodic_check(1):
                        my_GUI.bot.print_state()

                my_GUI.bot.run_state()
                time.sleep(0.1)
