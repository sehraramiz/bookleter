import pathlib
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
            'on_file_path_button_clicked': self.on_file_path_button_clicked,
            'on_file_path_button_clicked': self.on_file_path_button_clicked
            }

        builder.connect_callbacks(callbacks)

        combo = self.builder.get_object('book_direction_combobox')
        combo.bind("<<ComboboxSelected>>", self.on_book_direction_change) 

    def on_file_path_button_clicked(self):
        self.file_path = file_path = filedialog.askopenfilename(title="Select Pdf File")
        if file_path:
        self.builder.get_object('file_name_label').config(text=pathlib.Path(self.file_path).name)


    def on_book_direction_change(self, event):
        combo = self.builder.get_object('book_direction_combobox')
        self.book_direction = combo.get()


def gui_main():
    root = tk.Tk()
    app = Application(master=root)
    root.mainloop()

if __name__ == "__main__":
    gui_main()


