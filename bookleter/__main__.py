import sys, logging
from pathlib import Path, PurePath
from .Booklet import Book

def main():
    logging.basicConfig(level=logging.NOTSET)

    example_usage_command = """
        $ bookleter.py my_book.pdf 1-30 rtl 50
        $ bookleter.py [pdfname] [start_page-end_page] [direction: rtl ltr] [margin percentage: 50]
    """

    if len(sys.argv) < 5:
        logging.error("missing some arguments\nuse it like this:\n{}".format(example_usage_command))
        sys.exit()

    start_page_number = int(sys.argv[2].split("-")[0])
    end_page_number = int(sys.argv[2].split("-")[1])

    book_direction = sys.argv[3]

    margin_percentage = sys.argv[4]

    current_path = Path.cwd()
    file_path = PurePath.joinpath(current_path, sys.argv[1])
    temp_path = file_path.parent / 'tmp'
    Path(temp_path).mkdir(parents=True, exist_ok=True)

    NewBook = Book(file_path, start_page_number, end_page_number, book_direction, margin_percentage)
    NewBook.make_booklet()


if __name__ == '__main__':
    main()