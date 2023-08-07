import tkinter as tk
from random import randint
import platform                     # pip install platform
import threading
from playsound import playsound     # pip install playsound==1.2.2; if not okay, pip install wheel

TRACK_A = "wedding_music.mp3"
TRACK_B = "promises.mp3"

path = "./assets_scene/"

decor_lamps = path + "lamps.png"           # 370x370
decor_flowers = path + "flowers.png"       # 500x500

lamps_width, lamps_height = 370, 370
decor_width, decor_height = 500, 500

################################
# -=- - - - - - - - - - - - - -#
################################

def set(root):
    print(f"\n（一款小而美的屏幕保护程序，出品方：{make_string_in_dark_cyan('AsH')}{make_string_in_magenta('ki')}）\n")
    
    announce_wedding()
    install_lamps(root)
    paint_decor(root)
    music_start()
    
    print("\n———（双击兔兔退出屏保程序）———\n")
    
def announce_wedding():
    for i in range(7):
        print("Ash —=—=—=—=— ⭐ ❤ 新婚大禧 ❤ ⭐ —=—=—=—=— Qi")
    
    print("\n时间：2023.1.7")
    print("地点：\"Simple Love Coffee Home\", foot of Queen Elizabeth Park, 4936 Cambie St, Vancouver, BC V5Z 2Z5")
           
def install_lamps(root):
    screen_width, screen_height = get_screen_params()
    curr_x = 0
    
    while curr_x < screen_width:
        window = tk.Toplevel(root)
        window.geometry(f"{lamps_width}x{lamps_height}+{curr_x}+0")
        window.config(highlightbackground="black")
        window.overrideredirect(True)
        # window.attributes("-topmost", True)
        window.wm_attributes("-transparentcolor", "black")
        
        image_lamps = tk.PhotoImage(file=decor_lamps)

        label = tk.Label(window, image=image_lamps, bd=0, bg="black")
        label.image = image_lamps
        label.pack(side="left")
 
        curr_x += lamps_width + randint(-7, 177+77)
        
def paint_decor(root):
    screen_width, screen_height = get_screen_params()
    window = tk.Toplevel(root)
    
    decor_x = int(screen_width / 2 - decor_width / 2)
    decor_y = int(screen_height / 2 - decor_height / 2 + 30)
    window.geometry(f"{decor_width}x{decor_height}+{decor_x}+{decor_y}")
    
    window.config(highlightbackground="black")
    window.overrideredirect(True)
    # window.attributes("-topmost", True)
    window.wm_attributes("-transparentcolor", "black")
    
    image_decor = tk.PhotoImage(file=decor_flowers)
    
    label = tk.Label(window, image=image_decor, bd=0, bg="black")
    label.image = image_decor
    label.pack()
    
def music_start():
    music = select_music()
    
    if music:
        def play():
            while True:  # loop
                playsound(music, block=True)

        loop_thread = threading.Thread(target=play)
        loop_thread.daemon = True    # shut down when program exits
        loop_thread.start()
    
def select_music():
    music_path = None
    
    seed = randint(0, 2)
    if seed:
        print(f"正在播放：婚礼音乐CD {'A' if seed == 1 else 'B'}面")
        choice = TRACK_A if seed == 1 else TRACK_B
        music_path = path + choice
    else:
        print("正在播放：《The Sound of Silence》")
        
    return music_path

def get_screen_params():
    if platform.system() == "Windows":
        from win32api import GetMonitorInfo, MonitorFromPoint   # pip install pywin32
        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        work_area = monitor_info.get("Work")
        screen_width = work_area[2]
        work_height = work_area[3]
    elif platform.system() == "Darwin":
        from AppKit import NSScreen                             # pip install AppKit
        screen_width = NSScreen.mainScreen().frame().size.width
        work_height = NSScreen.mainScreen().frame().size.height
    else:
        expectation = "Expected: 'Linux' 'Windows' or 'Darwin', Received: "
        raise OSError(expectation + platform.system())
    
    return (screen_width, work_height)

def make_string_in_green(string):
    string_in_green = "\033[92m" + string + "\033[00m"
    return string_in_green

def make_string_in_dark_cyan(string):
    string_in_dark_cyan = "\033[36m" + string + "\033[00m"
    return string_in_dark_cyan

def make_string_in_magenta(string):
    string_in_magenta = "\033[95m" + string + "\033[00m"
    return string_in_magenta
