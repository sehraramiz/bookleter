import sys, logging, re
from pathlib import Path, PurePath
from bookleter import Booklet
from bookleter import gui

def main():
    logging.basicConfig(level=logging.NOTSET)

    example_usage_command = """
        $ bookleter my_book.pdf 1-30 rtl '50 50 50 50'
        $ bookleter [pdfname] [start_page-end_page] [direction: rtl ltr] [page crop: '50 50 50 50']
        direction: right to left (rtl) or left to right (ltr)
        page crop: amount of page border crop in pixels 'left top right bottom'
    """

    if len(sys.argv) == 1:
        gui.gui_main()
    elif len(sys.argv) < 5:
        logging.error("missing some arguments\nuse it like this:\n{}".format(example_usage_command))
        sys.exit()
    else:
        start_page_number = int(sys.argv[2].split("-")[0])
        end_page_number = int(sys.argv[2].split("-")[1])

        book_direction = sys.argv[3]

        if not re.match("\\d+ \\d+ \\d+ \\d+", sys.argv[4]):
            logging.error("invalid crop option\nuse it like this:\n{}".format(example_usage_command))
            sys.exit()
        crop_amount = [int(s) for s in re.findall(r'\b\d+\b', sys.argv[4])]

        crop = {
            "left": crop_amount[0],
            "top": crop_amount[1],
            "right": crop_amount[2],
            "bottom": crop_amount[3]
        }

        try:
            NewBook = Booklet.Book(sys.argv[1], start_page_number, end_page_number, book_direction, crop)
            NewBook.make_booklet()
        except IndexError:
            print("Page number out of range")
        except Exception as e:
            print(e)



if __name__ == '__main__':
    main()
