import tkinter as tk
from tkinter import filedialog, Text
import pygubu

class Application:
    def __init__(self, master=None):
        self.master = master
        
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('tkgui.ui')
        self.mainwindow = builder.get_object('mainwindow', master)
        builder.connect_callbacks(self)

        callbacks = {
            'on_file_path_button_clicked': self.on_file_path_button_clicked
            }

        builder.connect_callbacks(callbacks)

    def on_file_path_button_clicked(self):
        print("clicked!")

def gui_main():
    root = tk.Tk()
    app = Application(master=root)
    root.mainloop()

if __name__ == "__main__":
    gui_main()


