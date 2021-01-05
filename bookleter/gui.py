import os
from tkinter import *
from tkinter import ttk, messagebox, filedialog

from bookleter import Booklet
from bookleter.__version__ import __version__


pdf_file_path = ""

def browse_files():
    global pdf_file_path
    pdf_file_path = filedialog.askopenfilename(
        initialdir="",
        title="select a pdf file",
        filetypes=(
            ("pdf files","*.pdf*"),
        )
    )

    if pdf_file_path:
        file_name = os.path.basename(pdf_file_path)
        file_explorer_label.config(text=file_name)

def make_booklet():
    direction = direction_options.get()
    start_page_number = start_page_input.get()
    end_page_number = end_page_input.get()
    crop = {
        "left": crop_left_input.get(),
        "top": crop_top_input.get(),
        "right": crop_right_input.get(),
        "bottom": crop_bottom_input.get(),
    }
    try :
        new_book = Booklet.Book(
            pdf_file_path,
            start_page_number,
            end_page_number,
            direction,
            crop
        )
        new_book.make_booklet()
    except IndexError:
        messagebox.showerror("", "page number out of range")
        return
    except Exception as e:
        messagebox.showerror("", e)
        return

    messagebox.showinfo("", "your booklet is ready!")

window = Tk()
window.title(f"Bookleter {__version__}")
window.geometry('400x200')
window.option_add('*Font', '20')
window.configure(background = "white")
window.minsize(400, 200)

direction_label = Label(window ,text="Direction")
start_page_label = Label(window ,text="Start Page")
end_page_label = Label(window , text="End Page")
crop_label = Label(window , text="Crop")
file_explorer_label = Label(window, text="*.pdf")

direction_label.grid(row=1, column=0)
start_page_label.grid(row=2, column=0)
end_page_label.grid(row=3, column = 0)
crop_label.grid(row=4, column=0)
file_explorer_label.grid(row=6, column=0)

button_explore = Button(window, text="Open Pdf File", command=browse_files)
button_explore.grid(row=0, column=0)

start_page_input = Entry(window, width=5)
end_page_input = Entry(window, width=5)
crop_left_input = Entry(window, width=5)
crop_top_input = Entry(window, width=5)
crop_right_input = Entry(window, width=5)
crop_bottom_input = Entry(window, width=5)

direction_options = ttk.Combobox(window, values=["rtl", "ltr"], width=3)
direction_options.current(0)

direction_options.grid(row=1, column=1)
start_page_input.grid(row=2, column=1)
end_page_input.grid(row=3, column=1)
crop_left_input.grid(row=4, column=1)
crop_top_input.grid(row=4, column=2)
crop_right_input.grid(row=4, column=3)
crop_bottom_input.grid(row=4, column=4)

make_booklet_button = ttk.Button(window ,text="Make My Booklet", command=make_booklet).grid(row=5,column=0)

def gui_main():
    window.mainloop()

if __name__ == "__main__":
    gui_main()


