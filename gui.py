import tkinter as tk

class Gui(tk.Frame):

  def __init__(self, master, controller):
    super().__init__(master)
    self.master = master
    self.controller = controller

    # Schlüsselübersicht
    keysFrame = tk.Frame(self)

    btnFrame = tk.Frame(keysFrame)

    keyLabel = tk.Label(btnFrame, text="Deine Schlüssel")
    keyLabel.pack(side=tk.LEFT)

    newKeyBtn = tk.Button(btnFrame, text="+", command=controller.addKey)
    newKeyBtn.pack(side=tk.LEFT)

    deleteKeyBtn = tk.Button(btnFrame, text="-", command=controller.removeKey)
    deleteKeyBtn.pack(side=tk.LEFT)

    btnFrame.pack()

    self.keyBox = tk.Listbox(keysFrame)
    self.keyBox.pack(side=tk.BOTTOM)
    self.keyBox.bind("<<ListboxSelect>>", controller.on_key_selected)

    keysFrame.pack(side=tk.RIGHT)

    # de/encryptionfields
    leftFrame = tk.Frame(self)

    self.active_key_label = tk.Label(leftFrame, text="Kein Schlüssel ausgewählt")
    self.active_key_label.pack()

    self.text_field = tk.Text(leftFrame, height=10, width=50)
    self.text_field.pack()

    btnFrame = tk.Frame(leftFrame)

    decryptBtn = tk.Button(btnFrame, text="entschlüsseln", command=controller.decrypt)
    decryptBtn.pack(side=tk.RIGHT)

    encryptBtn = tk.Button(btnFrame, text="verschlüsseln", command=controller.encrypt)
    encryptBtn.pack(side=tk.RIGHT)

    saveBtn = tk.Button(btnFrame, text="speichern", command=controller.save)
    saveBtn.pack(side=tk.RIGHT)

    loadBtn = tk.Button(btnFrame, text="laden", command=controller.load)
    loadBtn.pack(side=tk.RIGHT)

    btnFrame.pack()
    
    leftFrame.pack()

    self.pack()

if __name__ == "__main__":
  window = tk.Tk()
  gui = Gui(window, None)
  tk.mainloop()