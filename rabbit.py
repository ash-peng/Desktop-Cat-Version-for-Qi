import tkinter as tk
import time
import random
from random import randint
import scene
import openai       # pip install openai

################################
# -=- - - - - - - - - - - - - -#
################################

# from pydub import AudioSegment
# from pydub.playback import play
# from resemble import Resemble
# import os
# from gtts import gTTS
    
################################
# -=- - - - - - - - - - - - - -#
################################

screen_width, work_height = scene.get_screen_params()

idle_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # 12: transition to sleep
sleep_num = [19, 20, 21, 22, 23, 24, 25]  # 26: transition to idle
walk_left = [13, 14, 15]
walk_right = [16, 17, 18]

USE_GPT = True      # switch on while use
THINK_FREQ = 237

PROMPT_1 = "You are a rabbit and today you are getting married to a deer. It is a cold, rainy day in January. The wedding venue is a small but cozy coffee shop at the foot of a green hill. During the wedding, you are going to play your guitar and the deer will sing. Please say something to the your bride in under 10 simple words while taking a stroll together in the park. If needed, refer to the bride by \"Kiki\". Say it in Chinese."
PROMPT_2 = "You are now a bridegroom. It is January, and the sky is raining lightly. Please say something under 15 simple English words, to the bride while walking around in your wedding venue - it is a coffee shop near a picturesque park, and on the wedding day you play the guitar and sing together with the bride. You are a rabbit and the bride is a deer. Please refer to the bride by \"Kiki\". Say it in Chinese."

# ENGL_MESSAGES = ["We are really getting married today. REALLY.",
#                  "I love this atmosphere and this music.",
#                  "I wish every day is simple and sweet like today.",
#                  "Kiki, my deer, my dear.",
#                  "I love those lights up there.",
#                  "I love you.",
#                  "Kiki, from this day on, you are my one and only, and I am your one and only...",
#                  "I want to pee.",
#                  "Que sera sera, whatever will be will be...",
#                  "Wherever we go, what matters is that we're together.",
#                  "I love you, Kiki.",
#                  "Kiki, kiss me in the rain...",
#                  "The ring looks so perfect on your left hand.",
#                  "Kiki, come here and sit with me...",
#                  "Wish our love never ends.",
#                  "Run, Kiki, run! :D",
#                  "I walk a straight line. You run freely around. This is our difference, but we love each other.",
#                  "Hey Kiki, do you want to come and sit with me?",
#                  "Kiki, do you like the music?",
#                  "Maybe marriage is a boring thing, but I will never be bored, because of you, because of our love.",
#                  "Today is the beginning of 'us'.",
#                  "Am I the 222nd rabbit in Yan'an, China?",
#                  "Let's make a wish together...",
#                  "Kiki, your voice is so beautiful and sexy.",
#                  "Sometimes I wish to go back in time and meet you when you were 7. You must have been so cute...",
#                  "Bring my wife a hot chocolate please, because she doesn't like coffee except Frappuccino.",
#                  "Hey Kiki, would you like to go on a date with me?",
#                  "The rain is beautiful, and so are you.",
#                  "Kiki, come here and hold my hand...",
#                  "Would be nice for us to take a walk in the park when this ends.",
#                  "Look at the guests! They are all LGBT...",
#                  "Kiki, my dearest deer.",
#                  "Who is this beautiful deer running by my side? It is my wife, Kiki.",
#                  "Enjoying this moment..."
#                 ]

INIT_MESSAGES = ["我们今天真的就结婚了吗。",
                 "我爱这音乐，我爱这世界……",
                 "希望今后的每天，\n都能像今天一样简单甜蜜。",
                 "Kiki, my deer, my dear.",
                 "我好喜欢上面的灯",
                 "姐姐，我爱你。",
                 "姐姐，从今天起，我只有你一个人，你也只有我一个人。",
                 "我想尿尿",
                 "Que sera sera, whatever will be, will be...",
                 "不论我们以后去哪，\n有你就是我们的家。",
                 "老婆，我爱你。",
                 "姐姐在雨里亲我。",
                 "老婆，这个戒指好适合你。",
                 "姐姐，过来坐我旁边好不好。",
                 "今天 == 永远，永远 == 今天",
                 "Run, Kiki, run :D",
                 "我喜欢沿着直线一路走，你喜欢偏离轨道随心而行，我们很多不同，但是我们相爱。",
                 "这匹鹿一直跳来跳去真的不会出汗吗？",
                 "Do you like this music?",
                 "也许婚姻大多平淡无趣，但因为你、因为我们相爱，生活永远不会无聊。",
                 "今天是“我们”的第一天。",
                 "我是温哥华的第222只兔子吗？",
                 "姐姐，我们一起许个愿好不好。",
                 "Why is your voice so sexy?",
                 "别踢我屁股老婆",
                 "我常常想，\n小时候的你会是怎么样子，\n如果能回到七岁的时候遇见你，\n一定很可爱。",
                 "麻烦帮新娘子把咖啡换成热可可，\n她喝咖啡只喝星冰乐。",
                 "Hey Kiki, would you like to go on a date with me?",
                 "The rain is beautiful, so are you.",
                 "姐姐过来，牵着我。",
                 "我们等这个结束去公园散步好不好。",
                 "Who is this beautiful deer running by my side? It is my wife, Kiki.",
                 "Suffering from marriage coma..."
                ]

# INIT_MESSAGES = ["我爱你"]  # for testing auto-generated messages


################################
# -=- - - - - - - - - - - - - -#
################################

class Rabbit:
    def __init__(self, root, folder_name="rabbit"):
        self.root = root
        self.window = tk.Toplevel(root)
        
        self.dialogue = tk.Toplevel(root)
        self.dialogue.bind("<Configure>", self.move_dialogue)
        self.dialogue.withdraw()
        
        self.messages = INIT_MESSAGES

        self.idle = [
            tk.PhotoImage(file="assets_" + folder_name + "/idle1.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/idle2.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/idle3.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/idle4.png"),
        ]

        self.idle_to_sleeping = [
            tk.PhotoImage(file="assets_" + folder_name + "/sleeping1.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/sleeping2.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/sleeping3.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/sleeping4.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/sleeping5.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/sleeping6.png"),
        ]

        self.sleeping = [
            tk.PhotoImage(file="assets_" + folder_name + "/zzz1.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/zzz2.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/zzz3.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/zzz4.png"),
        ]

        self.sleeping_to_idle = [
            tk.PhotoImage(file="assets_" + folder_name + "/sleeping6.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/sleeping5.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/sleeping4.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/sleeping3.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/sleeping2.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/sleeping1.png"),
        ]

        self.walking_left = [
            tk.PhotoImage(file="assets_" + folder_name + "/walkingleft1.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/walkingleft2.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/walkingleft3.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/walkingleft4.png"),
        ]

        self.walking_right = [
            tk.PhotoImage(file="assets_" + folder_name + "/walkingright1.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/walkingright2.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/walkingright3.png"),
            tk.PhotoImage(file="assets_" + folder_name + "/walkingright4.png"),
        ]
        
        self.thoughts = tk.PhotoImage(file="assets_" + folder_name + "/thoughts.png")

        self.x = int(screen_width * 0.618)
        self.y = work_height - 43

        self.i_frame = 0                    # iterator representing index of each element inside event arrays
        self.state = 1                      # 0 == idle, 1 == idle_to_sleeping, 2 == sleeping, 3 == sleeping_to_idle, 4 == walk_left, 5 == walk_right
        self.event_number = randint(1, 3)   # events from 1 to 25 in event arrays, initial value represents idle
        self.frame = self.idle[0]           # the png to place
        
        self.window.config(highlightbackground="black")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.wm_attributes("-transparentcolor", "black")
        
        self.dialogue.config(highlightbackground="black")
        self.dialogue.overrideredirect(True)
        self.dialogue.attributes("-topmost", True)
        self.dialogue.wm_attributes("-transparentcolor", "black")

        self.label = tk.Label(self.window, bd=0, bg="black")
        self.label.pack()
        self.dialogue_label = tk.Label(self.dialogue, bd=0, bg="black")
        self.dialogue_label.pack()
        
        self.window.bind('<Double-1>', self.quit)
        
        self.window.after(
            1, self.update, self.i_frame, self.state, self.event_number, self.x
        )

    def event(self, i_frame, state, event_number, x):
        if self.event_number in idle_num:
            self.state = 0
            self.window.after(
                400, self.update, self.i_frame, self.state, self.event_number, self.x
            )
        elif self.event_number == 12:   # idle to sleeping
            self.state = 1
            self.window.after(
                100, self.update, self.i_frame, self.state, self.event_number, self.x
            )
        elif self.event_number in walk_left:
            self.state = 4
            self.window.after(
                100, self.update, self.i_frame, self.state, self.event_number, self.x
            )
        elif self.event_number in walk_right:
            self.state = 5
            self.window.after(
                100, self.update, self.i_frame, self.state, self.event_number, self.x
            )
        elif self.event_number in sleep_num:
            self.state = 2
            self.window.after(
                400, self.update, self.i_frame, self.state, self.event_number, self.x
            )
        elif self.event_number == 26:   # sleeping to idle
            self.state = 3
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
        if randint(0, THINK_FREQ) == 7:
            self.think()
        
        if self.state == 0:
            self.frame = self.idle[self.i_frame] 
            self.i_frame, self.event_number = self.animate(
                self.i_frame, self.idle, self.event_number, 1, 18
            )   # idle -> idle, any frame of walk left or walk right, or idle_to_sleeping (12)
            
        elif state == 1:
            self.frame = self.idle_to_sleeping[self.i_frame]
            self.i_frame, self.event_number = self.animate(
                self.i_frame, self.idle_to_sleeping, self.event_number, 19, 19
            )   # idle_to_sleeping -> first frame of sleep
            
        elif self.state == 2:
            self.frame = self.sleeping[self.i_frame]
            self.i_frame, self.event_number = self.animate(
                self.i_frame, self.sleeping, self.event_number, 19, 26
            )   # sleeping -> any frame of sleep, or sleeping_to_idle (26)
            
        elif self.state == 3:
            self.frame = self.sleeping_to_idle[self.i_frame]
            self.i_frame, self.event_number = self.animate(
                self.i_frame, self.sleeping_to_idle, self.event_number, 1, 1
            )   # sleeping_to_idle -> first frame of idle
            
        elif self.state == 4 and self.x > 125:
            self.frame = self.walking_left[self.i_frame] 
            self.x -= randint(0, 8)
            
            keep_walking_next = randint(0, 3)
            if keep_walking_next:
                self.i_frame, self.event_number = self.animate(
                    self.i_frame, self.walking_left, self.event_number, 13, 15
                )   # walking_left -> walking_left
            else:
                self.i_frame, self.event_number = self.animate(
                    self.i_frame, self.walking_left, self.event_number, 1, 18
                )   # walking_left -> idle, any frame of walk left or walk right, or idle_to_sleeping (12)
            
        elif self.state == 5 and self.x < (screen_width - 125):
            self.frame = self.walking_right[self.i_frame] 
            self.x += randint(0, 8)
            
            keep_walking_next = randint(0, 3)
            if keep_walking_next:
                self.i_frame, self.event_number = self.animate(
                    self.i_frame, self.walking_right, self.event_number, 16, 18
                )   # walking_right -> walking_right
            else:
                self.i_frame, self.event_number = self.animate(
                    self.i_frame, self.walking_right, self.event_number, 1, 18
                )   # walking_right -> idle, any frame of walk left or walk right, or idle_to_sleeping (12) 
                
        else:
            # possibly stuck, move in random direction
            self.x += randint(-30, 30)
            self.frame = self.idle[self.i_frame] 
            self.i_frame, self.event_number = self.animate(
                self.i_frame, self.idle, self.event_number, 1, 26
            )       # anything would do

        self.window.geometry("80x43+" + str(self.x) + "+" + str(self.y))
        self.label.configure(image=self.frame)
           
        self.window.after(
            1, self.event, self.i_frame, self.state, self.event_number, self.x
        )

    def think(self):
        if len(self.messages) < 20:
            self.get_new_message()
            
        if self.dialogue.state() != "normal":   # if thought bubble not shown
            self.dialogue.deiconify()           # show thought bubble
            msg = self.messages.pop(randint(0, len(self.messages)-1))
            print("\nAsh产生了一个新的念头。.\n- \" " + scene.make_string_in_green(msg) + " \"")
            # self.speak(msg)
            self.dialogue.after(10000, self.close_dialogue) # after 10 seconds, hide thought bubble
            
            
        # # try to use resemble.ai to read message?
        
        # Resemble.api_key("Jraw581cbRGLS4YTNjQ2wgtt")
        # project_uuid = '424ce296'
        # voice_uuid = '970e2ebf'
        # body = message
  
        # response = Resemble.v2.clips.create_sync(
        #     project_uuid,
        #     voice_uuid,
        #     body,
        #     title="voice",
        #     sample_rate=44100,
        #     output_format="wav",
        #     include_timestamps=True
        # )
        
        # if response:
        #     print(response)
        # else:
        #     print("None")
        
    def get_new_message(self):
        if USE_GPT:
            openai.api_key = ""
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    temperature=1.314,
                    max_tokens=1000,
                    messages=[
                        {
                            "role": "user",
                            "content": PROMPT_1 if randint(0, 1) else PROMPT_2,
                        }
                    ],
                )
                message = response["choices"][0]["message"]["content"].strip("\"")
                
            except openai.error.ServiceUnavailableError:
                # message = "I love you."
                message = "我爱你。"
            
        else:
            # message = "Enjoying this moment..."
            message = "享受这一刻"
        
        self.messages.append(message)
        
    def speak(self, text):
        # myobj = gTTS(
        #     text=text,
        #     lang="en",
        #     tld="ie",
        #     slow=False
        # )
 
        # myobj.save("convert.wav")
        # os.system("convert.wav")
        
        pass
            
    def move_dialogue(self, event):
        # x, y = self.window.winfo_x(), self.window.winfo_y()
        self.dialogue.geometry(f"80x43+{self.x+19}+{self.y-23}")
        self.dialogue_label.configure(image=self.thoughts)
        
    def close_dialogue(self):
        self.dialogue.withdraw()
        
    def quit(self, event):                           
        # print("Falling down the rabbit hole") 
        print("\nAsh和Kiki掉进了兔子洞。\n")
        import sys; sys.exit() 
