import logging, shutil, sys
from pathlib import Path
from pathlib import Path, PurePath

from PyPDF2 import PdfFileWriter, PdfFileReader
from shuffle import foop
from pdfCropMargins import pdfCropMargins


class Book():
    def __init__(self, input_file_path, start_page_number, end_page_number, direction, margin_percentage='10'):
        # TODO add input validation
        current_path = Path.cwd()
        self.input_file_path = PurePath.joinpath(current_path, input_file_path)
        self.start_page_number = start_page_number
        self.end_page_number = end_page_number
        self.direction = direction
        self.margin_percentage = margin_percentage

        logging.basicConfig(level=logging.NOTSET)
        
        self.temp_path = self.input_file_path.parent / 'tmp'
        Path(self.temp_path).mkdir(parents=True, exist_ok=True)

        self.original_pdf_name = self.input_file_path.name
        self.original_pdf_path = str(self.input_file_path)
        self.basic_temp_pdf_path = str(self.temp_path / self.original_pdf_name)
        self.pickout_pages_pdf_name = self.basic_temp_pdf_path.replace(".pdf", "_{}_{}.pdf".format(start_page_number, end_page_number))
        self.pickout_test_pages_pdf_name = self.basic_temp_pdf_path.replace(".pdf", "_{}_{}.pdf".format(1, 8))
        self.reversed_pickout_test_pages_pdf_name = self.pickout_test_pages_pdf_name.replace(".pdf", "_reversed.pdf")
        self.blanked_pdf_name = self.pickout_pages_pdf_name.replace(".pdf", "_blanked.pdf")
        self.blanked_shuffled_pdf_name = self.blanked_pdf_name.replace(".pdf", "_shuffled.pdf")
        self.reversed_blanked_pdf_name = self.blanked_pdf_name.replace(".pdf", "_reversed.pdf")
        self.reversed_blanked_shuffled_pdf_name = self.reversed_blanked_pdf_name.replace(".pdf", "_shuffled.pdf")
        self.reversed_blanked_shuffled_test_pdf_name = self.reversed_blanked_pdf_name.replace(".pdf", "_test_shuffled.pdf")
        self.final_pdf_name = self.original_pdf_path.replace(".pdf", "_print_this.pdf")
        self.test_pdf_name = self.final_pdf_name.replace(".pdf", "_for_test.pdf")

    def make_booklet(self):
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

        print_order = foop(self.correct_pages_count)

        if self.direction == "rtl":
            logging.info("changing book direction to rtl...")
            self._reverse_pages_order()

            logging.info("shuffling pages order...\ncreating final pdf...")
            self._shuffle_pdf(self.reversed_blanked_shuffled_pdf_name, print_order)

            logging.info("setting  margins...")
            self._set_margins(self.reversed_blanked_shuffled_pdf_name, self.final_pdf_name)

        else:
            self._shuffle_pdf(self.blanked_shuffled_pdf_name, print_order)

            logging.info("setting  margins...")
            self._set_margins(self.blanked_shuffled_pdf_name, self.final_pdf_name)


        logging.info("creating test pdf...")
        self._pickout_pages(1, 8)

        if self.direction == "rtl":
            self._reverse_pages_order()

        print_order = foop(8)
        self._shuffle_pdf(self.test_pdf_name, print_order)

        # FIXME cannot use pdfCropMargins 2 times in a row, so test pdf margins are the same as before
        # self._set_margins(self.reversed_blanked_shuffled_test_pdf_name, self.test_pdf_name)

        logging.info("cleaning up...")
        shutil.rmtree(self.temp_path)

        logging.info("finished!")

    def _pickout_pages(self, start_page_number, end_page_number):
        inputpdf = PdfFileReader(open(self.original_pdf_path, "rb"))
        output = PdfFileWriter()
        for pg_number in range(start_page_number, end_page_number + 1):
            output.addPage(inputpdf.getPage(pg_number - 1))
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

    def _shuffle_pdf(self, output_pdf_name, ordered_pages):
        output = PdfFileWriter()
        if self.direction == "rtl":
            inputpdf = PdfFileReader(open(self.reversed_blanked_pdf_name, "rb"))
        else:
            inputpdf = PdfFileReader(open(self.blanked_pdf_name, "rb"))

        for pg_number in ordered_pages:
            output.addPage(inputpdf.getPage(pg_number - 1))
        with open(output_pdf_name, "wb") as output_stream:
            output.write(output_stream)

    def _calc_pdf_pages(self):
        if self.end_page_number % 8 == 0:
            correct_pages_count = self.end_page_number
        else:
            correct_pages_count = ((((self.end_page_number - self.start_page_number) + 1) // 8) + 1) * 8
        white_pages_count = correct_pages_count - self.end_page_number
        return correct_pages_count, white_pages_count

    def _set_margins(self, input_pdf_name, output_pdf_name):
        sys.argv = [
            sys.argv[0],
            '-p',
            self.margin_percentage,
            input_pdf_name,
            '-o',
            output_pdf_name
        ]
        try:
            pdfCropMargins.main()
        except SystemExit:
            pass

    def check_booklet_is_created(self):
        return Path(self.final_pdf_name).is_file() and Path(self.test_pdf_name).is_file()

    def __str__(self):
        return str({
            "pdf_file_path": self.input_file_path,
            "start_page": self.start_page_number,
            "end_page": self.end_page_number,
            "margins": self.margin_percentage,
            "book_direction": self.direction
        })