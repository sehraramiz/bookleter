from PyPDF2 import PdfFileWriter, PdfFileReader


def pickout_pages(input_pdf_name, output_pdf_name, start_page_number, end_page_number):
    inputpdf = PdfFileReader(open(input_pdf_name, "rb"))
    output = PdfFileWriter()
    for pg_number in range(start_page_number, end_page_number + 1):
        output.addPage(inputpdf.getPage(pg_number))
    with open(output_pdf_name, "wb") as outputStream:
        output.write(outputStream)
