import mss
import mss.tools
import time
import pyautogui
from pynput.keyboard import Key, Listener
import keyboard
import os, sys
from PIL import Image
import random

target_score = 300
score = 0
total_sequence_list = []
j = 0

def sleep(duration, get_now=time.perf_counter):
    now = get_now()
    end = now + duration
    while now < end:
        now = get_now()

def make_screenshot(x, y, q):
    global j
    with mss.mss() as sct:      
        region = {'top': y-450, 'left': x-100, 'width': 100*2, 'height': 450}
        img = sct.grab(region)
        j += 1
        mss.tools.to_png(img.rgb, img.size, output="lumberjack.png")

def read_pixel_color(x, y):
    global j
    im = Image.open("lumberjack.png")
    pix = im.load()
    width, height = im.size

    return pix[width/2, y*2-1]

def get_cursor_coordinates():
    x, y = pyautogui.position()
    return x, y

def double_press(button, press_count):
    i = 0
    while i < press_count:
        keyboard.press_and_release(button)
        i += 1

def perform_sequence(sequence_list):
    global score
    for button in sequence_list:
        #print(button)
        if score < target_score:
            double_press(button, 2)
            score += 2
    
def play_game(x,y):
    global total_sequence_list
    while score < target_score:
        sleep_time = 0.147
        sequence_list = []
        make_screenshot(x, y, 1)
        p = 450
        pixel_distance = 100
        
        while p > 0:
            #print(read_pixel_color(1, p))
            if read_pixel_color(1, p) == (155, 117, 66):
                #print("BRANCH!")
                sequence_list.append("left")
                total_sequence_list.append("left")
            else:
                #print("NO BRANCH")
                sequence_list.append("right")
                total_sequence_list.append("right")
            p -= pixel_distance

        print(sequence_list)
        perform_sequence(sequence_list)
        sleep(sleep_time)

def find_longest_sequence(items, string):
    max_seq = 0
    i = 1
    temp_max_seq = 1
    while i < len(items):
        if items[i] == string and items[i] == items[i-1]:
            temp_max_seq += 1
            if temp_max_seq > max_seq:
                max_seq = temp_max_seq
        elif items[i] != items[i-1]:
            temp_max_seq = 1
        i += 1
    return max_seq

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------

def on_press(key):
    global score
    
    if key == Key.space:
        x,y = get_cursor_coordinates()
        play_game(x,y)
        score = 0
        print("\n"+str(total_sequence_list))
        print("left: "+str(find_longest_sequence(total_sequence_list, 'left')))
        print("right: "+str(find_longest_sequence(total_sequence_list, 'right')))
        total_sequence_list.clear()

    if key == Key.cmd:
        x,y = get_cursor_coordinates()
        make_screenshot(x, y, 1)
        print("x:" +str(x))
        print("y:" +str(y))
        print("------------------")
        print(read_pixel_color(x,y))

    if key == Key.left:
        score += 1
        pass

    if key == Key.right:
        score += 1
        pass
        
    if key == Key.esc:
        return False

def on_release(key):
    pass

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
