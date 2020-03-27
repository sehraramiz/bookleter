import sys, logging
from pathlib import Path, PurePath
from bookleter.Booklet import Book
from bookleter.tkgui import gui_main

def main():
    logging.basicConfig(level=logging.NOTSET)

    example_usage_command = """
        $ bookleter my_book.pdf 1-30 rtl 50
        $ bookleter [pdfname] [start_page-end_page] [direction: rtl ltr] [margin percentage: 50]
        direction: right to left (rtl) or left to right (ltr)
        margin percentage: percentage of original pdf margins to reduce
    """

    if len(sys.argv) == 1:
        gui_main()
    elif len(sys.argv) < 5:
        logging.error("missing some arguments\nuse it like this:\n{}".format(example_usage_command))
        sys.exit()
    else:
        start_page_number = int(sys.argv[2].split("-")[0])
        end_page_number = int(sys.argv[2].split("-")[1])

        book_direction = sys.argv[3]

        margin_percentage = sys.argv[4]

        NewBook = Book(sys.argv[1], start_page_number, end_page_number, book_direction, margin_percentage)
        NewBook.make_booklet()



if __name__ == '__main__':
    main()