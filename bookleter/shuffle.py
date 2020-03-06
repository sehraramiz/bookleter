
"""
    Credits
    This part of the application uses an Open Source component.
    This function was ported from a go script originally
    You can find the source code of the open source project along with license information below.
    i am grateful to this developer for his/her contribution to open source.

    Project: (a6-booklet-on-a4) https://github.com/ERnsTL/a6-booklet-on-a4
    License (GNU General Public License v3.0) https://www.gnu.org/licenses/gpl-3.0.en.html 
"""

def foop(pages_count):
    if pages_count == 0:
        raise ValueError("Enter number of pages")
    
    if pages_count % 8 != 0:
        raise ValueError("number of pages must be multiple of 8")

    sheets_count = pages_count // 8

    a4_sheets = [{"front": [None for _ in range(4)], "back": [None for _ in range(4)] } for i in range(sheets_count)]
    cur_page = 1

    for sheet_number in range(sheets_count):
        # front
        a4_sheets[sheet_number]["front"][0] = cur_page
        cur_page += 1
        a4_sheets[sheet_number]["front"][1] = cur_page
        cur_page += 1
        a4_sheets[sheet_number]["front"][2] = cur_page
        cur_page += 1
        a4_sheets[sheet_number]["front"][3] = cur_page
        cur_page += 1

        # back
        a4_sheets[sheet_number]["back"][0] = cur_page
        cur_page += 1
        a4_sheets[sheet_number]["back"][1] = cur_page
        cur_page += 1
        a4_sheets[sheet_number]["back"][2] = cur_page
        cur_page += 1
        a4_sheets[sheet_number]["back"][3] = cur_page
        cur_page += 1

    # vertically rip in half horizontally
    a5_sheets = [{"front": [None for _ in range(2)], "back": [None for _ in range(2)]} for i in range(sheets_count * 2)]

    # top half
    for sheet_number in range(sheets_count):
        # front
        a5_sheets[sheet_number]["front"][0] = a4_sheets[sheet_number]["front"][0]
        a5_sheets[sheet_number]["front"][1] = a4_sheets[sheet_number]["front"][1]

        # back
        a5_sheets[sheet_number]["back"][0] = a4_sheets[sheet_number]["back"][0]
        a5_sheets[sheet_number]["back"][1] = a4_sheets[sheet_number]["back"][1]

    # bottom half
    for sheet_number in range(sheets_count):
        # front
        a5_sheets[sheets_count + sheet_number]["front"][0] = a4_sheets[sheet_number]["front"][2]
        a5_sheets[sheets_count + sheet_number]["front"][1] = a4_sheets[sheet_number]["front"][3]

        # back
        a5_sheets[sheets_count + sheet_number]["back"][0] = a4_sheets[sheet_number]["back"][2]
        a5_sheets[sheets_count + sheet_number]["back"][1] = a4_sheets[sheet_number]["back"][3]


    # number all physical pages in book order
    cur_page = 0

    # left pages of the stack going up = first half book pages
    book_order = [None for _ in range(pages_count)]
    for sheet_number in range(len(a5_sheets)):
        # back right
        book_order[cur_page] = a5_sheets[sheet_number]["back"][1]
        cur_page += 1
        # front left
        book_order[cur_page] = a5_sheets[sheet_number]["front"][0]
        cur_page += 1

    for sheet_number in reversed(range(len(a5_sheets))):
        # front right
        book_order[cur_page] = a5_sheets[sheet_number]["front"][1]
        cur_page += 1
        # back left
        book_order[cur_page] = a5_sheets[sheet_number]["back"][0]
        cur_page += 1

    # apply translation
    print_order = [None for _ in range(pages_count)]
    for index, pg_number in enumerate(book_order):
        print_order[pg_number - 1] = index + 1

    return print_order