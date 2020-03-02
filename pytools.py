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

def reverse_pages_order(input_pdf_name, output_pdf_name):
    output = PdfFileWriter()
    with open(input_pdf_name, 'rb') as readfile:
        inputpdf = PdfFileReader(readfile)
        for page in reversed(inputpdf.pages):
            output.addPage(page)
        with open(output_pdf_name, "wb") as output_stream:
            output.write(output_stream)

def shuffle_pdf(input_pdf_name, output_pdf_name, ordered_pages):
    output = PdfFileWriter()
    inputpdf = PdfFileReader(open(input_pdf_name, "rb"))
    # pages = range(inputpdf.getNumPages())
    # random.shuffle(pages)
    for pg_number in ordered_pages:
        output.addPage(inputpdf.getPage(pg_number - 1))
    with open(output_pdf_name, "wb") as output_stream:
        output.write(output_stream)

def calc_pdf_pages(start_page_number, end_page_number):
    if end_page_number % 8 == 0:
        correct_pages_count = end_page_number
    else:
        correct_pages_count = ((((end_page_number - start_page_number) + 1) // 8) + 1) * 8
    white_pages_count = correct_pages_count - end_page_number
    return correct_pages_count, white_pages_count