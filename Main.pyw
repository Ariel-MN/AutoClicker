#!/usr/bin/env python3

### AUTOCLICKER PROGRAM ###

import os
import sys
from datetime import datetime
from pynput import keyboard
from customtkinter import *
import threading
import subprocess
from Config import AutoRun

__version__ = 'v1.0.1'

AppPath = os.path.dirname(__file__)   

def WriteLog(Level, Message):
    # Write messages to log file
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(f"{AppPath}/autoclick.log", "a+") as f:
        f.write(f"{now} - [{Level}] {Message}\n")

ConfigTxt = ''

def ReadConfigFile():
    with open(os.path.join(AppPath,'config.txt'), '+r') as f:
        return f.read()

def SaveConfigFile(text):
    with open(os.path.join(AppPath,'config.txt'), '+w') as f:
        f.write(text)
    btn_save.configure(state=DISABLED, fg_color="steelblue4")


# Create Program GUI #
if __name__ == "__main__":
    params = sys.argv[1:]

    WindowHide = "--hide" in params
    AutoClickRun = "--run" in params

    Running = False

    try:
        # AutoClick thread
        exit_thread = threading.Event()
        def bg_thread():
            while not exit_thread.is_set():
                try:
                    AutoRun(ConfigTxt)
                except BaseException:
                    # BaseExceptions capture "TypeError" and "IndexError" errors, which are already handled in the Config unit.
                    program_stop(None)

        # Window settings
        Root = CTk()
        Root.title(f"AutoClicker - {__version__}")
        Root.geometry("340x150")
        Root.minsize(340,160)
        #ImgPath = os.path.join(AppPath,'img')
        #Root.iconbitmap(os.path.join(ImgPath,'Favicon.ico'))
        
        # Run the program minimized if start with --hide parameter
        if WindowHide:
            Root.iconify()

        # Get current window size
        RootWidth = Root.winfo_screenwidth()
        RootHeight = Root.winfo_screenheight()

        # Custom fonts
        FontTitle=("Segoe UI",22,"bold")
        FontSubTitle=("Segoe UI",16,"bold")
        FontBody=("Segoe UI",14,"normal")
        FontBodyBold=("Segoe UI",14,"bold")
        FontConfig=("Consolas",14,"normal")

        # Custom colors light and dark theme
        primary=('#009faa', '#29f7ff')
        primary2=('#19a8b2', '#28e2e9')
        secondary=('#fdfdfd', '#323232')
        secondary2=('#f9f9f9', '#393939')
        tertiary=('#fefefe', '#3e3e3e')
        tertiary2=('#f2f2f2', '#494949')
        quaternary=('#8a8a8a', '#9d9d9d')

        # Create GUI components
        tabview = CTkTabview(Root, text_color=primary, width=RootWidth, height=RootHeight, corner_radius=10, segmented_button_fg_color=tertiary,
                             segmented_button_selected_color=tertiary2, segmented_button_unselected_color=secondary, segmented_button_selected_hover_color=secondary,
                             segmented_button_unselected_hover_color=secondary2)
        tabview.pack(padx=10, pady=(0,10), anchor=N)

        tabview.add("Run")
        tabview.add("Config")
        tabview.set("Run")  # set currently visible tab

        # Run page components
        frame_run = CTkFrame(master=tabview.tab("Run"))
        frame_run.pack(padx=5, pady=5)

        btn_play = CTkButton(master=frame_run, text="Play", fg_color="green yellow", text_color='#323232', text_color_disabled='#323232', hover_color=primary, font=FontBodyBold)
        btn_stop = CTkButton(master=frame_run, text="Stop", fg_color="light coral", text_color='#323232', text_color_disabled='#323232', hover_color=primary, font=FontBodyBold)
        lbl_status = CTkLabel(master=tabview.tab("Run"), text="Status: Initialized", font=FontBody)
        btn_play.pack(padx=5, pady=5, side=LEFT, expand=True)
        btn_stop.pack(padx=5, pady=5, side=LEFT, expand=True)
        lbl_status.pack(padx=5, pady=5, anchor=S)

        # Config page components
        frame_conf = CTkFrame(master=tabview.tab("Config"))
        frame_conf.pack(padx=5, pady=5, fill=X, anchor=N)

        btn_tool = CTkButton(master=frame_conf, text="Tool", fg_color="steelblue1", text_color='#323232', text_color_disabled='#323232', hover_color=primary, font=FontBodyBold)
        btn_save = CTkButton(master=frame_conf, text="Save", state=DISABLED, fg_color="steelblue4", text_color='#323232', text_color_disabled='#323232', hover_color=primary,
                             font=FontBodyBold, command=lambda: SaveConfigFile(txb_config.get('0.0',END)))
        btn_tool.pack(padx=5, pady=5, side=LEFT)
        btn_save.pack(padx=5, pady=5, side=RIGHT)

        txb_config = CTkTextbox(master=tabview.tab("Config"), font=FontConfig)
        txb_config.pack(padx=5, pady=5, fill=BOTH, expand=True, anchor=S)

        # Load config file text into TextBox component
        ConfigTxt = ReadConfigFile()
        txb_config.insert(INSERT, ConfigTxt)

        # Create tk window event handlers
        def program_stop(event):
            global Running
            if Running:
                lbl_status.configure(text = "Status: Stoped")
                exit_thread.set() # close thread after current cicle
                Running=False

        def program_play(event):
            global Running
            if not Running:
                lbl_status.configure(text = "Status: Running")
                thread = threading.Thread(target=bg_thread) # create thread
                exit_thread.clear() # clear thread exit event
                thread.start()
                Running=True

        def tool_handle(event):
            subprocess.call(f'gnome-terminal --geometry=40x3+4000+0 --title="Tool for window and mouse location" -- watch -n0.1 xdotool getmouselocation', shell=True)

        def save_handle(event):
            # Enable button save when the focus is on the TextBox object and a keyboard key is pressed
            btn_save.configure(state=NORMAL, fg_color="steelblue1")

        # Bind event handler to button click
        btn_play.bind("<Button-1>",program_play)
        btn_stop.bind("<Button-1>",program_stop)
        btn_tool.bind("<Button-1>",tool_handle)
        txb_config.bind("<Key>",save_handle)

        # Bind event handler to key pressed
        def on_press(key):
            # Start with keys F6 and home (inizio)
            if key in [keyboard.Key.f6,keyboard.Key.home]:
                program_play(None)
            # Stop with keys F7 and end (fine)
            elif key in [keyboard.Key.f7,keyboard.Key.end]:
                program_stop(None)
        # Listen in a thread for the keys pressed even if the tk window is not focused
        listener = keyboard.Listener(
            on_press=on_press)
        listener.start()

        # Program on close event
        def on_closing():
            exit_thread.set()
            Root.destroy()
        Root.protocol("WM_DELETE_WINDOW", on_closing)

        # Run the AutoClick if program start with --run parameter
        if AutoClickRun:
            program_play(None)

        # Run the GUI main loop
        Root.mainloop()

    except Exception as E:
        WriteLog('Error', E)
