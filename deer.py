import tkinter as tk
import time
import random
from random import randint
import scene
from PIL import Image, ImageTk  # pip install pillow

################################
# -=- - - - - - - - - - - - - -#
################################

screen_width, work_height = scene.get_screen_params()

walk_left = [13, 14, 15]
walk_right = [16, 17, 18]

APPROACH_FREQ = 47
SPAWN_FREQ = 7777

################################
# -=- - - - - - - - - - - - - -#
################################

class Deer:
    def __init__(self, root, loved_one=None, folder_name="deer", is_baby=False):
        self.root = root
        self.loved_one = loved_one
        self.is_baby = is_baby
        
        self.window = tk.Toplevel(root)
        
        walking_left_images = [
            Image.open("assets_" + folder_name + "/walkingleft1.png"),
            Image.open("assets_" + folder_name + "/walkingleft2.png"),
            Image.open("assets_" + folder_name + "/walkingleft3.png"),
            Image.open("assets_" + folder_name + "/walkingleft4.png"),
            Image.open("assets_" + folder_name + "/walkingleft5.png"),
            Image.open("assets_" + folder_name + "/walkingleft6.png"),
            Image.open("assets_" + folder_name + "/walkingleft7.png"),
            Image.open("assets_" + folder_name + "/walkingleft8.png"),
        ]
        
        walking_right_images = [
            Image.open("assets_" + folder_name + "/walkingright1.png"),
            Image.open("assets_" + folder_name + "/walkingright2.png"),
            Image.open("assets_" + folder_name + "/walkingright3.png"),
            Image.open("assets_" + folder_name + "/walkingright4.png"),
            Image.open("assets_" + folder_name + "/walkingright5.png"),
            Image.open("assets_" + folder_name + "/walkingright6.png"),
            Image.open("assets_" + folder_name + "/walkingright7.png"),
            Image.open("assets_" + folder_name + "/walkingright8.png"),
        ]
        
        if is_baby:
            # make smaller frames
            for i in range(len(walking_left_images)):
                walking_left_images[i] = walking_left_images[i].resize((40, 22))
            for i in range(len(walking_right_images)):
                walking_right_images[i] = walking_right_images[i].resize((40, 22))
        
        self.walking_left, self.walking_right = [], []
        for image in walking_left_images:
            self.walking_left.append(ImageTk.PhotoImage(image))
        for image in walking_right_images:
            self.walking_right.append(ImageTk.PhotoImage(image))
            
        if is_baby:
            # spawn where the parent is
            self.x = self.loved_one.x
            self.y = self.loved_one.y
        else:
            self.x = int(screen_width * 0.618)
            self.y = work_height - 43

        self.i_frame = 0                    # iterator representing index of each element inside event arrays
        self.state = 4                      # 4 == walk_left, 5 == walk_right
        self.event_number = 13              # events from 13 to 18 in event arrays, initial value represents walking left
        self.frame = self.walking_left[0]   # the png to place
        
        self.window.config(highlightbackground="black")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.wm_attributes("-transparentcolor", "black")

        self.label = tk.Label(self.window, bd=0, bg="black")
        self.label.pack()
        
        self.window.bind('<Double-1>', self.quit)
        self.window.after(
            1, self.update, self.i_frame, self.state, self.event_number, self.x
        )

    def event(self, i_frame, state, event_number, x):
        if self.event_number in walk_left:
            self.state = 4
            self.window.after(
                100, self.update, self.i_frame, self.state, self.event_number, self.x
            )
        elif self.event_number in walk_right:
            self.state = 5
            self.window.after(
                100, self.update, self.i_frame, self.state, self.event_number, self.x
            )

    def animate(self, i_frame, array, event_number, a, b):
        # prepare i_frame and event_number for the next move
        if self.i_frame < len(array) - 1:
            # if movement not complete yet, proceed with next png
            self.i_frame += 1
        else:
            # start with next event, which can be somewhat random (depending on previous state)
            self.i_frame = 0
            self.event_number = randint(a, b)
        return self.i_frame, self.event_number

    def update(self, i_frame, state, event_number, x):
        if not self.is_baby and randint(0, SPAWN_FREQ) == 7:
            self.spawn()
            
        if randint(0, APPROACH_FREQ) == 7:
            self.approach_loved_one()
        
        if self.state == 4 and self.x > 20:
            self.frame = self.walking_left[self.i_frame]
            self.x -= randint(10, 40) if self.is_away_from_loved_one() else randint(3, 10)
            self.y += randint(-4, 2) if self.y > work_height / 2 else randint(-2, 4)
            
            self.i_frame, self.event_number = self.animate(
                    self.i_frame, self.walking_left, self.event_number, 13, 18
                )   # walking_left -> anything
            
        elif self.state == 5 and self.x < screen_width - 125:
            self.frame = self.walking_right[self.i_frame] 
            self.x += randint(10, 40) if self.is_away_from_loved_one() else randint(3, 10)
            self.y += randint(-4, 2) if self.y > work_height / 2 else randint(-2, 4)
            
            self.i_frame, self.event_number = self.animate(
                    self.i_frame, self.walking_right, self.event_number, 13, 18
                )   # walking_right -> anything
            
        elif self.x < 20:
            # reached left, move right
            self.frame = self.walking_right[self.i_frame]
            
            self.x += randint(10, 40) if self.is_away_from_loved_one() else randint(3, 10)
            self.y += randint(-4, 2) if self.y > work_height / 2 else randint(-2, 4)
                
            self.i_frame, self.event_number = self.animate(
                self.i_frame, self.walking_right, self.event_number, 16, 16
            )   # walking_left -> walking_right
            
        elif self.x > screen_width - 125:
            # reached right, move left
            self.frame = self.walking_left[self.i_frame]
            self.x -= randint(10, 40) if self.is_away_from_loved_one() else randint(3, 10)
            self.y += randint(-4, 2) if self.y > work_height / 2 else randint(-2, 4)
            self.i_frame, self.event_number = self.animate(
                self.i_frame, self.walking_left, self.event_number, 13, 13
            )   # walking_right -> walking_left
                
        else:
            # possibly stuck, move in random direction
            self.frame = self.walking_left[self.i_frame]
            self.x -= randint(-30, 30)
            self.y += randint(-5, 5)
            self.i_frame, self.event_number = self.animate(
                self.i_frame, self.walking_left, self.event_number, 13, 18
            )   # anything would do

        self.window.geometry("80x43+" + str(self.x) + "+" + str(self.y))
        if self.is_baby:
            self.window.geometry("40x22+" + str(self.x) + "+" + str(self.y))
        
        self.label.configure(image=self.frame)
           
        self.window.after(
            1, self.event, self.i_frame, self.state, self.event_number, self.x
        )
        
    def approach_loved_one(self):
        if abs(self.loved_one.x - self.x) < 80:
            return
        
        if not self.is_away_from_loved_one():
            return
        
        self.window.attributes("-topmost", True)

        if self.x < self.loved_one.x:
            # loved one is to the right of self
            self.frame = self.walking_right[self.i_frame]    
            self.state = 5
            self.x += randint(20, 50)
            self.i_frame, self.event_number = self.animate(
                self.i_frame, self.walking_right, self.event_number, 16, 16
            )
        else:
            # loved one is to the left of self
            self.frame = self.walking_left[self.i_frame]
            self.state = 4
            self.x -= randint(20, 50)
            self.i_frame, self.event_number = self.animate(
                self.i_frame, self.walking_left, self.event_number, 13, 13
            )
        
        self.y -= 20 if self.y > self.loved_one.y else -20
           
        self.label.configure(image=self.frame)
        
        self.window.after(
            100, self.approach_loved_one
        )
    
    def is_away_from_loved_one(self):
        return abs(self.loved_one.x - self.x) > 25 or abs(self.loved_one.y - self.y) > 25
    
    def spawn(self):
        Deer(self.root, self, is_baby=True)
    
    def quit(self, event):                           
        print("Jumping into eternity...") 
        import sys; sys.exit() 
