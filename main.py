import tkinter as tk
from rabbit import Rabbit
from deer import Deer
import scene

################################
# -=- - - - - - - - - - - - - -#
################################

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()     # hide main window
    
    scene.set(root)
    rabbit = Rabbit(root)
    deer = Deer(rabbit.window, rabbit)
    
    root.mainloop()
    