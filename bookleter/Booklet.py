import logging, subprocess, shutil
from pathlib import Path
from PyPDF2 import PdfFileWriter, PdfFileReader
from .shuffle import foop


class Book():
    def __init__(self, input_file_path, start_page_number, end_page_number, direction, margins):
        self.input_file_path = input_file_path
        self.start_page_number = start_page_number
        self.end_page_number = end_page_number
        self.direction = direction
        self.margins = margins

        logging.basicConfig(level=logging.NOTSET)
        
        self.temp_path = self.input_file_path.parent / 'tmp'
        Path(self.temp_path).mkdir(parents=True, exist_ok=True)

        self.original_pdf_name = self.input_file_path.name
        self.original_pdf_path = str(self.input_file_path)
        self.margined_pdf_name = str(self.temp_path / self.original_pdf_name.replace(".pdf", "_margined.pdf"))
        self.pickout_pages_pdf_name = self.margined_pdf_name.replace(".pdf", "_{}_{}.pdf".format(start_page_number, end_page_number))
        self.pickout_test_pages_pdf_name = self.margined_pdf_name.replace(".pdf", "_{}_{}.pdf".format(1, 8))
        self.reversed_pickout_test_pages_pdf_name = self.pickout_test_pages_pdf_name.replace(".pdf", "_reversed.pdf")
        self.blanked_pdf_name = self.pickout_pages_pdf_name.replace(".pdf", "_blanked.pdf")
        self.reversed_blanked_pdf_name = self.blanked_pdf_name.replace(".pdf", "_reversed.pdf")
        self.final_pdf_name = self.original_pdf_path.replace(".pdf", "_print_this.pdf")
        self.test_pdf_name = self.final_pdf_name.replace(".pdf", "_for_test.pdf")

    def make_booklet(self):
        self._check_requirments()
        logging.info("setting  margins...")
        self._set_margin_crop()
        logging.info("picking out desired pages...")
        self._pickout_pages(self.start_page_number, self.end_page_number)

        self.end_page_number = (self.end_page_number - self.start_page_number) + 1
        self.start_page_number = 1

        self.correct_pages_count, self.blank_pages_count = self._calc_pdf_pages()

        if self.blank_pages_count:
            logging.info("adding blank pages...")
            self._append_blank_pages()
        else:
            logging.info("no need for extra blank pages...")
            self.blanked_pdf_name = self.pickout_pages_pdf_name

        if self.direction == "rtl":
            logging.info("changing book direction to rtl...")
            self._reverse_pages_order()

        logging.info("shuffling pages order...\ncreating final pdf...")
        print_order = foop(self.reversed_blanked_pdf_name, self.final_pdf_name, self.correct_pages_count)
        self._shuffle_pdf(print_order)

        logging.info("creating test pdf...")
        self._pickout_pages(1, 8)

        if self.direction == "rtl":
            self._reverse_pages_order()

        print_order = foop(self.reversed_pickout_test_pages_pdf_name, self.test_pdf_name, 8)
        self._shuffle_pdf(print_order)
        
        logging.info("cleaning up...")
        shutil.rmtree(self.temp_path)

        logging.info("finished!")

    def _pickout_pages(self, start_page_number, end_page_number):
        inputpdf = PdfFileReader(open(self.margined_pdf_name, "rb"))
        output = PdfFileWriter()
        for pg_number in range(start_page_number, end_page_number + 1):
            output.addPage(inputpdf.getPage(pg_number))
        with open(self.pickout_pages_pdf_name, "wb") as output_stream:
            output.write(output_stream)

    def _append_blank_pages(self):
        inputpdf = PdfFileReader(open(self.pickout_pages_pdf_name, "rb"))
        output = PdfFileWriter()
        output.appendPagesFromReader(inputpdf)
        for i in range(self.blank_pages_count):
            output.addBlankPage()
        with open(self.blanked_pdf_name, "wb") as output_stream:
            output.write(output_stream)

    def _reverse_pages_order(self):
        output = PdfFileWriter()
        with open(self.blanked_pdf_name, 'rb') as readfile:
            inputpdf = PdfFileReader(readfile)
            for page in reversed(inputpdf.pages):
                output.addPage(page)
            with open(self.reversed_blanked_pdf_name, "wb") as output_stream:
                output.write(output_stream)

    def _shuffle_pdf(self, ordered_pages):
        output = PdfFileWriter()
        inputpdf = PdfFileReader(open(self.reversed_blanked_pdf_name, "rb"))
        for pg_number in ordered_pages:
            output.addPage(inputpdf.getPage(pg_number - 1))
        with open(self.final_pdf_name, "wb") as output_stream:
            output.write(output_stream)

    def _calc_pdf_pages(self):
        if self.end_page_number % 8 == 0:
            correct_pages_count = self.end_page_number
        else:
            correct_pages_count = ((((self.end_page_number - self.start_page_number) + 1) // 8) + 1) * 8
        white_pages_count = correct_pages_count - self.end_page_number
        return correct_pages_count, white_pages_count

    def _set_margin_crop(self):
        ## set margin or crop
        ## '10 7 10 7' --> 'left top right bottom'
        ## example command: pdfcrop in.pdf out.pdf --margins '10 7 10 7'
        margin_command = "pdfcrop {} {} --margins '{}'".format(self.original_pdf_path, self.margined_pdf_name, self.margins)
        subprocess.call([
            margin_command,
            ], shell=True)
    
    def _check_requirments(self):
        requirments = ["pdfcrop"]
        for req in requirments:
            if not shutil.which(req):
                raise ValueError("you have to install {} on your system".format(req))
    