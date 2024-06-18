#!/usr/bin/env python3

### AUTOCLICKER UTILS ###

import os
import time
import subprocess

# Get the path of this script file
AppPath=os.path.dirname(__file__)

def WriteLog(Level, Message):
    # Write messages to log file
    with open(f"{AppPath}/autoclick.log", "a+") as f:
        f.write(f"{Level}: {Message}")

# Custom automation functions #

def Delay(seconds='0',*args):
    time.sleep(int(seconds))

def LeftClick(x,y,delay='0',*args):
    Error = subprocess.call(f"xdotool mousemove {x} {y} && xdotool click 1 && sleep {delay}", shell=True)
    if Error:
        WriteLog("Warning", "Function LeftCLick xdotool Error: "+Error)

def RightClick(x,y,delay='0',*args):
    Error = subprocess.call(f"xdotool mousemove {x} {y} && xdotool click 3 && sleep {delay}", shell=True)
    if Error:
        WriteLog("Warning", "Function RightCLick xdotool Error: "+Error)

def WriteText(text,delay='0',*args):
    Error = subprocess.call(f'xdotool type "{text}" && sleep {delay}', shell=True)
    if Error:
        WriteLog("Warning", "Function WriteText xdotool Error: "+Error)

def PressKeys(keys, delay='0',*args):
    Error = subprocess.call(f'xdotool key {keys} && sleep {delay}', shell=True)
    if Error:
        WriteLog("Warning", "Function PressKeys xdotool Error: "+Error)

def SwitchToLeftDesktop(delay='0',*args):
    Error = subprocess.call(f'xdotool key ctrl+alt+Left && sleep {delay}', shell=True)
    if Error:
        WriteLog("Warning", "Function SwitchToLeftDesktop xdotool Error: "+Error)

def SwitchToRightDesktop(delay='0',*args):
    Error = subprocess.call(f'xdotool key ctrl+alt+Right && sleep {delay}', shell=True)
    if Error:
        WriteLog("Warning", "Function SwitchToRightDesktop xdotool Error: "+Error)
