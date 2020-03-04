import sys
from pathlib import Path, PurePath
from .Booklet import Book

def main():
    print('in main')
    args = sys.argv[1:]
    print('count of args :: {}'.format(len(args)))
    for arg in args:
        print('passed argument :: {}'.format(arg))

    example_usage_command = """
        $ bookleter.py my_book.pdf 1-30 rtl '5 5 5 5'
        $ bookleter.py [pdfname] [start_page-end_page] [direction: rtl ltr] [margins: 'left top right bottom']
    """

    if len(sys.argv) < 5:
            print("Error!! missing some arguments\nuse it like this:")
            print(example_usage_command)
            sys.exit()
    if sys.argv[1][-4:] == ".pdf":
        print(sys.argv)

    start_page_number = int(sys.argv[2].split("-")[0])
    end_page_number = int(sys.argv[2].split("-")[1])

    book_direction = sys.argv[3]

    margins = sys.argv[4]

    current_path = Path.cwd()
    file_path = PurePath.joinpath(current_path, sys.argv[1])
    temp_path = file_path.parent / 'tmp'
    Path(temp_path).mkdir(parents=True, exist_ok=True)

    NewBook = Book(file_path, start_page_number, end_page_number, book_direction, margins)
    NewBook.make_booklet()


if __name__ == '__main__':
    main()