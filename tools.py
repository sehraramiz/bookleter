import subprocess
from shuffle import foop


def pickout_pages(input_pdf_name, start_page_number, end_page_number, output_pdf_name):
    ## say we want to extract pages 1 to 100
    ## example command: pdftk in.pdf cat 1-100 output out.pdf
    pickout_pages_command = "pdftk {} cat {}-{} output {}".format(input_pdf_name, start_page_number, end_page_number, output_pdf_name)
    subprocess.call([
        pickout_pages_command,
        ], shell=True)

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