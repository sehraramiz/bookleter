#!/bin/python3

import subprocess, sys


if len(sys.argv) < 3:
        print("error")
        sys.exit()
if sys.argv[1][-4:] == ".pdf":
    print(sys.argv)

start_page_number = int(sys.argv[2].split("-")[0])
end_page_number = int(sys.argv[2].split("-")[1])

original_pdf_name = sys.argv[1]
margined_pdf_name = original_pdf_name.replace(".pdf", "_margined.pdf")
pickout_pages_pdf_name = margined_pdf_name.replace(".pdf", "_{}_{}.pdf".format(start_page_number, end_page_number))
blanked_pdf_name = pickout_pages_pdf_name.replace(".pdf", "_blanked.pdf")
final_pdf_name = original_pdf_name.replace(".pdf", "_print_this.pdf")

## set margin or crop
## '10 7 10 7' --> 'left top right bottom'
## example command: pdfcrop in.pdf out.pdf --margins '10 7 10 7'
margin_command = "pdfcrop {} {}".format(original_pdf_name, margined_pdf_name)
margin_command_options = "--margins '10 7 10 7'" 
subprocess.call([
    margin_command,
    margin_command_options
    ], shell=True)


## extract pages 1 to 109
## example command: pdftk in.pdf cat 1-109 output out.pdf
pickout_pages_command = "pdftk {} cat {}-{} output {}".format(margined_pdf_name, start_page_number, end_page_number, pickout_pages_pdf_name)
subprocess.call([
    pickout_pages_command,
    ], shell=True)


## calc pdf pages
correct_pages_count = ((((end_page_number - start_page_number) + 1) // 8) + 1) * 8
white_pages_count = correct_pages_count - end_page_number

## add n white pages to pdf
## example command: pdftk A=in.pdf B=blank.pdf cat A1-end B B B output out.pdf
B = "B " * white_pages_count
add_white_pages_command = "pdftk A={} B=blank.pdf cat A1-end {} output {}".format(pickout_pages_pdf_name, B, blanked_pdf_name)
subprocess.call([
    add_white_pages_command,
    ], shell=True)


## get final shuffled pdf with 128 pages and get output
## example command:  ~/go/bin/a6-booklet-on-a4 -in in.pdf -out out.pdf -pages 128
get_final_booklet_pdf_command = "~/go/bin/a6-booklet-on-a4 -in {} -out {} -pages {}".format(blanked_pdf_name, final_pdf_name,correct_pages_count)
pdftk_shuffle_command = subprocess.check_output([
    get_final_booklet_pdf_command,
    ], shell=True).decode().replace("\n", "")

subprocess.call([
    pdftk_shuffle_command,
    ], shell=True)