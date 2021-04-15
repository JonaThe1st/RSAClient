import tkinter as tk
from functools import partial

class DialogBox(object):

    def __init__(self, master, msg, btns):
        self.top = tk.Toplevel(master)
        self.btns = btns

        tk.Label(self.top, text=msg).pack()

        btnsFrame = tk.Frame(self.top)
        for key in btns.keys():
          callback = partial(self.processCommand, (key))
          tk.Button(btnsFrame, text=key, command=callback).pack()

        btnsFrame.pack()

    def processCommand(self, key):
      self.btns[key]()
      self.top.destroy()
      self.top.update()


if __name__ == "__main__":
  root = tk.Tk()

  tk.Button(root, text="haha", command=lambda: DialogBox(root, "was", {"dflgksd": lambda: print("test")})).pack()

  root.mainloop()