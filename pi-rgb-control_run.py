# Published under GPL v3 by Dominik Brand on 2023-02-11
# Version 1.0
# Tested with Raspberry Pi 3b and Arduino Uno + Mega
import tkinter as tk
import serial
from tkinter.colorchooser import askcolor
from tkinter import Tk, Canvas, Frame, BOTH, messagebox
import string
import os
import subprocess
import random
import time
from time import sleep, strftime

def time():
    timeStr = strftime('%H:%M')
    lbl_time.config(text = timeStr)
    lbl_time.after(1000, time)
def date():
    dateStr = strftime('%Y-%m-%d')
    lbl_date.config(text = dateStr)
    lbl_date.after(10000, date)
def day():
    dayStr = strftime('%A')
    lbl_day.config(text = dayStr)
    lbl_day.after(10000, day)
def hex2rgb(hexColor):
    rgb = hexColor.lstrip('#')
    rgb_ = tuple(int(rgb[i:i+2], 16) for i in (0, 2, 4))
    rgbColor = str(rgb_).replace(",", "").replace("(", "").replace(")", "")
    rgb_array = rgbColor.split(" ")
    return(rgb_array)
def rgb2hex(r,g,b):
    hexColor = '#%02x%02x%02x' % (r,g,b)
    return(hexColor)
def modes(modeChoice):
    mode = modeChoice
    serialCom(mode,0,0,0)
def fullscrn(fullScreen):
    fullscreen_btn.destroy()
    if(fullScreen == False):
        fullScreen = True
        window.attributes('-fullscreen',fullScreen)
def color_picker(isSet, r, g, b):
    rgb_array=[0,0,0]
    mode = "COLOR"
    if(isSet == 0):
        colors = askcolor(title="Tkinter Color Chooser")
        hexColor = colors[1]
        if colors[0] != None:
            rgb_array = hex2rgb(colors[1])
    elif(isSet == 1):
        rgb_array[0] = r
        rgb_array[1] = g
        rgb_array[2] = b
        hexColor = rgb2hex(r,g,b)
    serialCom(mode,rgb_array[0],rgb_array[1],rgb_array[2])
def serialCom(mode, r, g, b):
    received = ""
    while("ACK" not in received):
        openSerial.write(str.encode(mode+","+str(r)+","+str(g)+","+str(b)))
        received = str(openSerial.readline())
        sleep(1)
def main():
    global window
    window = tk.Tk()
    window.title("Neopixel color changer")
    window.resizable(width=True, height=True)
    window.geometry("800x480")
    window.configure(background="#111111")
    fullScreen = False
    btn_pick_color_0 = tk.Button(master=window, text="", bg='#FF0055', activebackground="#DD0033", height=3, width=12, command=(lambda: color_picker(1,255,0,20)))
    btn_pick_color_0.grid(row=0, column=1, sticky="w", padx=3, pady=0)
    btn_pick_color_1 = tk.Button(master=window, text="", bg='#009900', activebackground="#007700", height=3, width=12, command=(lambda: color_picker(1,0,255,0)))
    btn_pick_color_1.grid(row=0, column=2, sticky="w", padx=3, pady=0)
    btn_pick_color_2 = tk.Button(master=window, text="", bg='#0000FF', activebackground="#000088", height=3, width=12, command=(lambda: color_picker(1,0,0,255)))
    btn_pick_color_2.grid(row=0, column=3, sticky="w", padx=3, pady=0)
    btn_pick_color_3 = tk.Button(master=window, text="", bg='#00FFFF', activebackground="#00AAAA", height=3, width=12, command=(lambda: color_picker(1,0,255,255)))
    btn_pick_color_3.grid(row=0, column=4, sticky="w", padx=3, pady=0)
    btn_pick_color_4 = tk.Button(master=window, text="", bg='#AAFF00', activebackground="#77AA00", height=3, width=12, command=(lambda: color_picker(1,200,230,0)))
    btn_pick_color_4.grid(row=1, column=1, sticky="w", padx=3, pady=0)
    btn_pick_color_5 = tk.Button(master=window, text="", bg='#FFFF00', activebackground="#AAAA00", height=3, width=12, command=(lambda: color_picker(1,255,100,0)))
    btn_pick_color_5.grid(row=1, column=2, sticky="w", padx=3, pady=0)
    btn_pick_color_6 = tk.Button(master=window, text="", bg='#FF0000', activebackground="#AA0000", height=3, width=12, command=(lambda: color_picker(1,255,0,0)))
    btn_pick_color_6.grid(row=1, column=3, sticky="w", padx=3, pady=0)
    btn_pick_color_7 = tk.Button(master=window, text="", bg='#FFFFFF', activebackground="#CCCCCC", height=3, width=12, command=(lambda: color_picker(1,255,255,255)))
    btn_pick_color_7.grid(row=1, column=4, sticky="w", padx=3, pady=0)
    btn_pick_color_8 = tk.Button(master=window, text="", bg='#FFFF88', activebackground="#CCCC55", height=3, width=12, command=(lambda: color_picker(1,255,200,100)))
    btn_pick_color_8.grid(row=2, column=1, sticky="w", padx=3, pady=0)
    btn_pick_color_9 = tk.Button(master=window, text="", bg='#2088FF', activebackground="#106688", height=3, width=12, command=(lambda: color_picker(1,50,180,255)))
    btn_pick_color_9.grid(row=2, column=2, sticky="w", padx=3, pady=0)
    btn_pick_color_10 = tk.Button(master=window, text="", bg='#8800FF', activebackground="#6600AA", height=3, width=12, command=(lambda: color_picker(1,140,0,255)))
    btn_pick_color_10.grid(row=2, column=3, sticky="w", padx=3, pady=0)
    btn_pick_color_11 = tk.Button(master=window, text="", bg='#444444', activebackground="#222222", height=3, width=12, command=(lambda: color_picker(1,44,44,44)))
    btn_pick_color_11.grid(row=2, column=4, sticky="w", padx=3, pady=0)
    btn_pick_color = tk.Button(master=window, text="Pick color", bg='#888888', activebackground='#333333', height=3, width=7, command=(lambda: color_picker(0,0,0,0)))
    btn_pick_color.grid(row=3, column=0, sticky="w", padx=3, pady=0)
    rand_color_btn = tk.Button(master=window, text="Rainbow", bg='#888888', activebackground='#333333', height=3, width=7, command=(lambda: modes("RAINBOW")))
    rand_color_btn.grid(row=5, column=0, sticky="w", padx=3, pady=0)
    solid_loop_btn = tk.Button(master=window, text="Starfall", bg='#888888', activebackground='#333333', height=3, width=7, command=(lambda: modes("STARFALL")))
    solid_loop_btn.grid(row=2, column=0, sticky="w", padx=3, pady=0)
    rand_color_btn = tk.Button(master=window, text="OFF", bg='#888888', activebackground='#333333', height=3, width=7, command=(lambda: color_picker(1,0,0,0)))
    rand_color_btn.grid(row=0, column=0, sticky="w", padx=3, pady=0)
    global fullscreen_btn
    fullscreen_btn = tk.Button(master=window, text="FULLSCREEN", bg='#888888', activebackground='#333333', height=3, width=7, command=(lambda: fullscrn(fullScreen)))
    fullscreen_btn.grid(row=0, column=5, sticky="e", padx=3, pady=0)
    exit_btn = tk.Button(master=window, text="Exit", bg='#555555', activebackground='#333333', height=3, width=7, command=(lambda: window.destroy()))
    exit_btn.grid(row=6, column=0, sticky="e", padx=3, pady=0)
    global lbl_serial
    lbl_serial = tk.Label(master=window, font= ('calibri', 12), background="#111111", foreground='#CC0088')
    lbl_serial.grid(row=7, column=0, sticky="w", padx=0, pady=0)
    global lbl_time
    lbl_time = tk.Label(master=window, font= ('calibri', 30), background="#111111", foreground='#CC0088')
    lbl_time.grid(row=7, column=3, sticky="w", padx=0, pady=0)
    global lbl_date
    lbl_date = tk.Label(master=window, font= ('calibri', 20), background="#111111", foreground='#CC0088')
    lbl_date.grid(row=7, column=4, sticky="w", padx=0, pady=0)
    global lbl_day
    lbl_day = tk.Label(master=window, font= ('calibri', 20), background="#111111", foreground='#CC0088')
    lbl_day.grid(row=7, column=5, sticky="w", padx=0, pady=0)
    colorCycleBtn = tk.Button(master=window, text="Colorcycle", bg='#888888', activebackground='#333333', height=3, width=7, command=(lambda: modes("CYCLE")))
    colorCycleBtn.grid(row=1, column=0, sticky="w", padx=3, pady=0)
    time()
    date()
    day()
    window.mainloop()
if __name__ == '__main__':
    global openSerial
    try:
        openSerial = serial.Serial('/dev/ttyACM1')
    except:
        openSerial = serial.Serial('/dev/ttyACM0')
    openSerial.baudrate = 2400
    main()