from keyfactory import getRandomKeyPair, RSAPrivate, RSAPublic
from filehandler import saveKeyPair, loadKeyPair, loadKey, saveKey, saveString, loadString
from gui import Gui
from customDialog import DialogBox
from util import get_all_files

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askinteger, askstring
from tkinter.messagebox import askyesno
import os, json

class Rsa:
    def __init__(self):
        window = tk.Tk()

        self.activeKey = None
        self.keys = {}

        self.gui = Gui(window, self)

        self.loadKeys()
    
    def save(self):
        content = self.gui.text_field.get("0.0", tk.END)
        filename = askopenfilename()

        if filename is not None:
            saveString(filename, content)

    def load(self):
        filename = askopenfilename()
        
        self.gui.text_field.delete("0.0", tk.END)

        if filename is not None:
            content = loadString(filename)
            self.gui.text_field.insert("0.0", content)

    def decrypt(self):
        content = self.gui.text_field.get("0.0", tk.END)

        if self.activeKey is None:
            print("no active key")
            return

        key = self.activeKey["keys"]
        if self.activeKey["kind"] == "pair":
            key = self.activeKey["keys"][0]

        try:
            blocks = json.loads(content)
            decrypted = key.getStringFromBlocks(key.applyToBlocks(blocks))

            self.gui.text_field.delete("0.0", tk.END)

            #decrypted.replace(" ")
            decrypted = decrypted.replace("\x00", "")
            decrypted = decrypted[:len(decrypted)-1]
            print(decrypted)

            

            self.gui.text_field.insert(tk.END, str(decrypted))

        except json.JSONDecodeError:
            print("no valid blocks")
        


    def encrypt(self):
        content = self.gui.text_field.get("0.0", tk.END)

        if self.activeKey is None:
            print("no active key")
            return
        
        key = self.activeKey["keys"]
        if self.activeKey["kind"] == "pair":
            key = self.activeKey["keys"][1]

        blocks = key.applyToBits(content.encode())
        self.gui.text_field.delete("0.0", tk.END)

        print(blocks)

        self.gui.text_field.insert(tk.END, str(blocks))

    def addKey(self):
        opts = {
            "Aus bestehender Datei": self.newKeyFromFile,
            "Zufälliger Schlüssel": self.newRandKey,
            "Parameter eingeben": self.newKeyParams,
        }

        DialogBox(self.gui.master, "Du hast drei Möglichkeiten", opts)

    def newRandKey(self):
        bit_length = askinteger("Schlüssellänge", "Gib die Bitlänge des Schlüssels an")
        name = askstring("Schlüsselname", "Gib dem Schlüssel einen Namen")
        if bit_length != None and name != None and not name in self.keys.keys():
            key_pair = getRandomKeyPair(bit_length)
            self.keys[name] = {"keys": key_pair, "kind": "pair"}   
            saveKeyPair(key_pair, f"keys/{name}.key")
            self.reloadKeys()

    def newKeyFromFile(self):
        filename = askopenfilename()

        if filename is not None:
            self.loadKeyFromFile(filename)

        self.reloadKeys()

    def newKeyParams(self):
        print("Not availlable")

    def removeKey(self):
        key_box = self.gui.keyBox
        selected_key= key_box.curselection()[0]
        
        key_name = key_box.get(selected_key)

        if not askyesno(message=f"Bist du sicher, dass du den Schlüssel {key_name} löschen willst?"):
            return

        key_box.delete(selected_key)

        try:
            os.remove(f"keys/{key_name}.key")
        except FileNotFoundError:
            pass

        key = self.keys[key_name]
        if (key == self.activeKey):
            self.activeKey = None
            self.gui.active_key_label.configure(text="Kein Schlüssel ausgewählt")

        self.keys.pop(key_name)

    def loadKeys(self):
        if not os.path.exists("keys"):
            os.mkdir("keys")
            return

        files = get_all_files("keys/")
        
        for key in files:
            key_name = self.loadKeyFromFile(f"keys/{key}")

            self.gui.keyBox.insert(0, key_name)

    def loadKeyFromFile(self, path):
        key_name = path.split(".")[0].split("/")
        key_name = key_name[len(key_name) - 1]

        if key_name in self.keys.keys():
            print("name vergeben")
            return

        private_key, public_key = loadKeyPair(path)
        if not private_key and not public_key:
            print("keynotfound")
            return
            
        if private_key is None:
            kind = "public"
            keys = public_key
            saveKey(public_key, f"keys/{key_name}.key")
        if public_key is None:
            kind = "private"
            keys = private_key
            saveKey(private_key, f"keys/{key_name}.key")
        else:
            kind = "pair"
            keys = (private_key, public_key)
            saveKeyPair(keys, f"keys/{key_name}.key")

        self.keys[key_name] = {"keys": keys, "kind": kind}
        return key_name

    def reloadKeys(self):
        self.gui.keyBox.delete(0, tk.END)
        for key in self.keys.keys():
            self.gui.keyBox.insert(0, key)

    def on_key_selected(self, event):
        try:
            key_name = self.gui.keyBox.get(self.gui.keyBox.curselection()[0])
            self.activeKey = self.keys[key_name]
            self.gui.active_key_label.configure(text=f"Aktiver Schlüssel: {key_name}")
        except IndexError:
            pass

if __name__ == "__main__":
    rsa = Rsa()

    tk.mainloop()