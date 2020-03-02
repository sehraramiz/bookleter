import random
from PyPDF2 import PdfFileWriter, PdfFileReader


def pickout_pages(input_pdf_name, output_pdf_name, start_page_number, end_page_number):
    inputpdf = PdfFileReader(open(input_pdf_name, "rb"))
    output = PdfFileWriter()
    for pg_number in range(start_page_number, end_page_number + 1):
        output.addPage(inputpdf.getPage(pg_number))
    with open(output_pdf_name, "wb") as output_stream:
        output.write(output_stream)

def append_blank_pages(input_pdf_name, output_pdf_name, blanK_pages_count):
    inputpdf = PdfFileReader(open(input_pdf_name, "rb"))
    output = PdfFileWriter()
    output.appendPagesFromReader(inputpdf)
    for i in range(blanK_pages_count):
        output.addBlankPage()
    with open(output_pdf_name, "wb") as output_stream:
        output.write(output_stream)
        output.write(outputStream)
