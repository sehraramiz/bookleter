import subprocess
from shuffle import foop


def pickout_pages(input_pdf_name, start_page_number, end_page_number, output_pdf_name):
    ## say we want to extract pages 1 to 100
    ## example command: pdftk in.pdf cat 1-100 output out.pdf
    pickout_pages_command = "pdftk {} cat {}-{} output {}".format(input_pdf_name, start_page_number, end_page_number, output_pdf_name)
    subprocess.call([
        pickout_pages_command,
        ], shell=True)

def set_margin_crop(input_pdf_name, output_pdf_name, margin):
    ## set margin or crop
    ## '10 7 10 7' --> 'left top right bottom'
    ## example command: pdfcrop in.pdf out.pdf --margins '10 7 10 7'
    margin_command = "pdfcrop {} {} --margins '{}'".format(input_pdf_name, output_pdf_name, margin)
    subprocess.call([
        margin_command,
        ], shell=True)

def create_blank_pdf(blank_pdf_name):
    ## create a blank pdf file
    create_blank_pdf_command = "convert xc:none -page Letter {}".format(blank_pdf_name)
    subprocess.call([
        create_blank_pdf_command,
        ], shell=True)

def calc_pdf_pages(start_page_number, end_page_number):## calc pdf pages
    if end_page_number % 8 == 0:
        correct_pages_count = end_page_number
    else:
        correct_pages_count = ((((end_page_number - start_page_number) + 1) // 8) + 1) * 8
    white_pages_count = correct_pages_count - end_page_number
    return correct_pages_count, white_pages_count


def reverse_pages_order(pdf_name, reversed_pdf_name):
    ## reverse pdf pages order for rtl languages
    reverse_pages_order_command = "pdftk {} cat end-1 output {}".format(pdf_name, reversed_pdf_name)
    subprocess.call([
        reverse_pages_order_command,
        ], shell=True)

def make_booklet(input_pdf_name, output_pdf_name, pages_count):
    get_final_booklet_pdf_command = foop(input_pdf_name, output_pdf_name, pages_count)
    pdftk_shuffle_command = subprocess.check_output([
        get_final_booklet_pdf_command,
        ], shell=True).decode().replace("\n", "")

    subprocess.call([
        pdftk_shuffle_command,
        ], shell=True)