from Tkinter import *

class Application():
    def __init__(self, root):
        self.root = root
        self.categories =   [
                                "",
                                "",
                                "",
                            ]
root = Tk()
app = Application(root)
root.mainloop()
#root.destroy()
