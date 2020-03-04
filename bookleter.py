#!/bin/python3

import subprocess, sys
from pathlib import Path, PurePath
from shuffle import foop
from pytools import pickout_pages as pick, append_blank_pages, reverse_pages_order as reverse, shuffle_pdf as shuffle, calc_pdf_pages
from tools import set_margin_crop, check_requirments


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

# check if user has the needed software
check_requirments()

start_page_number = int(sys.argv[2].split("-")[0])
end_page_number = int(sys.argv[2].split("-")[1])

book_direction = sys.argv[3]

margins = sys.argv[4]

current_path = Path.cwd()
file_path = PurePath.joinpath(current_path, sys.argv[1])
temp_path = file_path.parent / 'tmp'
Path(temp_path).mkdir(parents=True, exist_ok=True)

# not very important file names
original_pdf_name = file_path.name
original_pdf_path = str(file_path)
margined_pdf_name = str(temp_path / original_pdf_name.replace(".pdf", "_margined.pdf"))
pickout_pages_pdf_name = margined_pdf_name.replace(".pdf", "_{}_{}.pdf".format(start_page_number, end_page_number))
pickout_test_pages_pdf_name = margined_pdf_name.replace(".pdf", "_{}_{}.pdf".format(1, 8))
reversed_pickout_test_pages_pdf_name = pickout_test_pages_pdf_name.replace(".pdf", "_reversed.pdf")
blanked_pdf_name = pickout_pages_pdf_name.replace(".pdf", "_blanked.pdf")
reversed_blanked_pdf_name = blanked_pdf_name.replace(".pdf", "_reversed.pdf")
final_pdf_name = original_pdf_path.replace(".pdf", "_print_this.pdf")
test_pdf_name = final_pdf_name.replace(".pdf", "_for_test.pdf")

set_margin_crop(original_pdf_path, margined_pdf_name, margins)

# pickout only desired pages from original pdf
pick(margined_pdf_name, pickout_pages_pdf_name, start_page_number, end_page_number)

end_page_number = (end_page_number - start_page_number) + 1
start_page_number = 1

correct_pages_count, blank_pages_count = calc_pdf_pages(start_page_number, end_page_number)

if blank_pages_count:
    append_blank_pages(pickout_pages_pdf_name, blanked_pdf_name, blank_pages_count)
else:
    blanked_pdf_name = pickout_pages_pdf_name

if book_direction == "rtl":
    reverse(blanked_pdf_name, reversed_blanked_pdf_name)

print_order = foop(reversed_blanked_pdf_name, final_pdf_name, correct_pages_count)
shuffle(reversed_blanked_pdf_name, final_pdf_name, print_order)

# create a 8 page pdf for testing the printer device and print method before printing big chunks of paper
# extract pages 1 to 8 for 8 page test
pick(margined_pdf_name, pickout_test_pages_pdf_name, 1, 8)

if book_direction == "rtl":
    reverse(pickout_test_pages_pdf_name, reversed_pickout_test_pages_pdf_name)

print_order = foop(reversed_pickout_test_pages_pdf_name, test_pdf_name, 8)
shuffle(reversed_pickout_test_pages_pdf_name, test_pdf_name, print_order)

shutil.rmtree(temp_path)