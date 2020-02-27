#!/bin/python3

import subprocess, sys, pathlib
from tools import pickout_pages, reverse_pages_order, make_booklet


if len(sys.argv) < 4:
        print("missing some arguments")
        sys.exit()
if sys.argv[1][-4:] == ".pdf":
    print(sys.argv)


start_page_number = int(sys.argv[2].split("-")[0])
end_page_number = int(sys.argv[2].split("-")[1])

current_path = pathlib.Path.cwd()
temp_path = str(current_path) + "/tmp/"
pathlib.Path(temp_path).mkdir(parents=True, exist_ok=True)

# not very important file names
original_pdf_name = sys.argv[1]
margined_pdf_name = temp_path + original_pdf_name.replace(".pdf", "_margined.pdf")
pickout_pages_pdf_name = margined_pdf_name.replace(".pdf", "_{}_{}.pdf".format(start_page_number, end_page_number))
pickout_test_pages_pdf_name = margined_pdf_name.replace(".pdf", "_{}_{}.pdf".format(1, 8))
reversed_pickout_test_pages_pdf_name = pickout_test_pages_pdf_name.replace(".pdf", "_reversed.pdf")
blanked_pdf_name = pickout_pages_pdf_name.replace(".pdf", "_blanked.pdf")
reversed_blanked_pdf_name = blanked_pdf_name.replace(".pdf", "_reversed.pdf")
blank_pdf_name = temp_path + "/blank.pdf"
final_pdf_name = original_pdf_name.replace(".pdf", "_print_this.pdf")
test_pdf_name = final_pdf_name.replace(".pdf", "_for_test.pdf")
blank_pdf_name = temp_path + "/blank.pdf"

## set margin or crop
## '10 7 10 7' --> 'left top right bottom'
## example command: pdfcrop in.pdf out.pdf --margins '10 7 10 7'
## FIXME margin command option is not working
margin_command = "pdfcrop {} {} --margins '7 7 7 7'".format(original_pdf_name, margined_pdf_name)
margin_command_options = "--margins '10 7 10 7'" 
subprocess.call([
    margin_command,
    # margin_command_options
    ], shell=True)

# pickout only desired pages from original pdf
pickout_pages(margined_pdf_name, start_page_number, end_page_number, pickout_pages_pdf_name)


## calc pdf pages
if end_page_number % 8 == 0:
    correct_pages_count = end_page_number
else:
    correct_pages_count = ((((end_page_number - start_page_number) + 1) // 8) + 1) * 8
white_pages_count = correct_pages_count - end_page_number

## create a blank pdf file
create_blank_pdf_command = "convert xc:none -page Letter {}".format(blank_pdf_name)
subprocess.call([
    create_blank_pdf_command,
    ], shell=True)


## add n white pages to pdf
## example command: pdftk A=in.pdf B=blank.pdf cat A1-end B B B output out.pdf
if white_pages_count:
    B = "B " * white_pages_count
    add_white_pages_command = "pdftk A={} B={} cat A1-end {} output {}".format(pickout_pages_pdf_name, blank_pdf_name, B, blanked_pdf_name)
    subprocess.call([
        add_white_pages_command,
        ], shell=True)
else:
    blanked_pdf_name = pickout_pages_pdf_name


## TODO get pdf language from input
reverse_pages_order(blanked_pdf_name, reversed_blanked_pdf_name)

## get final shuffled pdf with 128 pages and get output
make_booklet(reversed_blanked_pdf_name, final_pdf_name, correct_pages_count)

## create a 8 page pdf for testing the printer device and print method before printing big chunks of paper
## extract pages 1 to 8 for 8 page test
pickout_pages(margined_pdf_name, 1, 8, pickout_test_pages_pdf_name)

reverse_pages_order(pickout_test_pages_pdf_name, reversed_pickout_test_pages_pdf_name)

make_booklet(reversed_pickout_test_pages_pdf_name, test_pdf_name, 8)


## Cleanup
cleanup_command = "rm -r {}".format(temp_path)
subprocess.call([
    cleanup_command,
    ], shell=True)