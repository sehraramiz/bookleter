import pathlib, webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox, Menu, Label, Toplevel
import pygubu
from bookleter import Booklet
from bookleter.__version__ import __version__

class Application:
    def __init__(self, master=None):
        self.master = master
        
        self.builder = builder = pygubu.Builder()
        current_path = pathlib.Path(__file__).parent.absolute()
        tkui_path = current_path / 'bookleter.ui'
        builder.add_from_file(tkui_path)
        self.mainwindow = builder.get_object('mainwindow', master)
        builder.connect_callbacks(self)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        infoMenu = Menu(menu)
        menu.add_cascade(label="Hey", menu=infoMenu)
        infoMenu.add_command(label="About", command=self.show_about)

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

        self.crop = {
            'left': "",
            'top': "",
            'right': "",
            'bottom': ""
        }

        self.builder.get_object('crop_left').insert(0, 'left')
        self.builder.get_object('crop_top').insert(0, 'top')
        self.builder.get_object('crop_right').insert(0, 'right')
        self.builder.get_object('crop_bottom').insert(0, 'bottom')

        for entry_id in ["crop_left", "crop_top", "crop_right", "crop_bottom"]:
            self.set_placeholder(entry_id)

        self.book_direction_index = 0


    def set_placeholder(self, entry_id):
        entry = self.builder.get_object(entry_id)
        entry.bind("<FocusIn>", lambda event, arg={"entry": entry, "placeholder": entry.get()}: self.foc_in(event, arg))
        entry.bind("<FocusOut>", lambda event, arg={"entry": entry, "placeholder": entry.get()}: self.foc_out(event, arg))

    def put_placeholder(self, entry, placeholder):
        entry.insert(0, placeholder)

    def foc_in(self, *args):
        try:
            int(args[1]['entry'].get())
        except Exception:
            args[1]['entry'].delete('0', 'end')

    def foc_out(self, *args):
        if not args[1]['entry'].get():
            self.put_placeholder(args[1]['entry'], args[1]['placeholder'])


    def on_file_path_button_clicked(self):
        self.file_path = file_path = filedialog.askopenfilename(title="Select Pdf File")
        if file_path:
            self.builder.get_object('file_name_label').config(text=pathlib.Path(self.file_path).name)

    def on_make_booklet_button_clicked(self):
        self.start_page_number = self.builder.get_object('start_page_input').get()
        self.end_page_number = self.builder.get_object('end_page_input').get()
        self.crop["left"] = self.builder.get_object('crop_left').get()
        self.crop["top"] = self.builder.get_object('crop_top').get()
        self.crop["right"] = self.builder.get_object('crop_right').get()
        self.crop["bottom"] = self.builder.get_object('crop_bottom').get()

        direction_options = ["rtl", "ltr"]

        # make booklet
        try :
            new_book = Booklet.Book(
                self.file_path,
                self.start_page_number,
                self.end_page_number,
                direction_options[self.book_direction_index],
                self.crop
            )
            new_book.make_booklet()
        except IndexError:
            messagebox.showerror("", "Page number out of range")
            return
        except Exception as e:
            messagebox.showerror("", e)
            return
        
        messagebox.showinfo("", "Your Booklet Is Ready!")
    
    def on_book_direction_change(self, event):
        combo = self.builder.get_object('book_direction_combobox')
        self.book_direction_index = combo.current()

    def show_about(self):
        ABOUT_TEXT = "The Bookleter {} ".format(__version__)
        toplevel = Toplevel(borderwidth=50)
        
        about_label = Label(toplevel, text=ABOUT_TEXT, height=0, width=0)
        about_label.pack()
        
        github_link = Label(toplevel, text="Bookleter on Github", fg="blue", cursor="hand2", pady=5)
        github_link.pack()
        github_link.bind("<Button-1>", lambda e: self.callback("http://github.com/reinenichts/bookleter"))

        virgool_link = Label(toplevel, text="About Booklets", fg="blue", cursor="hand2", pady=5)
        virgool_link.pack()
        virgool_link.bind("<Button-1>", lambda e: self.callback("https://virgool.io/@mohsenbarzegar/bookleter-nkkuh18xnbyk"))

        new_version_link = Label(toplevel, text="New Version", fg="blue", cursor="hand2", pady=5)
        new_version_link.pack()
        new_version_link.bind("<Button-1>", lambda e: self.callback("https://github.com/reinenichts/bookleter/releases"))

        button = tk.Button(
            toplevel, 
            text="Cool", 
            fg="black",
            command=toplevel.destroy
            )
        button.pack()

    def callback(self, url):
        webbrowser.open(url)


def gui_main():
    root = tk.Tk()
    root.minsize(300, 400)
    app = Application(master=root)
    root.mainloop()

if __name__ == "__main__":
    gui_main()


