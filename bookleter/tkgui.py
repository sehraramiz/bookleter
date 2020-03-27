import pathlib
import tkinter as tk
from tkinter import filedialog, Text, messagebox
import pygubu
from .Booklet import Book


class Application:
    def __init__(self, master=None):
        self.master = master
        
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('tkgui.ui')
        self.mainwindow = builder.get_object('mainwindow', master)
        builder.connect_callbacks(self)

        callbacks = {
            'on_file_path_button_clicked': self.on_file_path_button_clicked,
            'on_make_booklet_button_clicked': self.on_make_booklet_button_clicked
            }

        builder.connect_callbacks(callbacks)

        combo = self.builder.get_object('book_direction_combobox')
        combo.bind("<<ComboboxSelected>>", self.on_book_direction_change)

        self.file_path = ""
        self.start_page_number = ""
        self.end_page_number = ""
        self.margins = ""
        self.book_direction_index = ""


    def on_file_path_button_clicked(self):
        self.file_path = file_path = filedialog.askopenfilename(title="Select Pdf File")
        if file_path:
            self.builder.get_object('file_name_label').config(text=pathlib.Path(self.file_path).name)

    def on_make_booklet_button_clicked(self):
        self.start_page_number = self.builder.get_object('start_page_input').get()
        self.end_page_number = self.builder.get_object('end_page_input').get()
        self.margins = self.builder.get_object('margins_input').get()

        direction_options = ["rtl", "ltr"]

        # make booklet
        if self.validate_inputs():
            new_book = Book(
                self.file_path,
                int(self.start_page_number),
                int(self.end_page_number),
                direction_options[self.book_direction_index],
                self.margins
            )
            print(new_book)
            new_book.make_booklet()
        else:
            print("invalid")
            return
        
        if not new_book.check_booklet_is_created():
            messagebox.showwarning("Sorry", "Please Reastart The App For Another booklet :>")
            return
        
        messagebox.showinfo("", "Your Booklet Is Ready!")
    
    def validate_inputs(self):
        if "" in [
            self.file_path, self.start_page_number,
            self.end_page_number, str(self.book_direction_index),
            self.margins
            ]:
            return False
        return True

    def on_book_direction_change(self, event):
        combo = self.builder.get_object('book_direction_combobox')
        self.book_direction_index = combo.current()


def gui_main():
    root = tk.Tk()
    app = Application(master=root)
    root.mainloop()

if __name__ == "__main__":
    gui_main()


