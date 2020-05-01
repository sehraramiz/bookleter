import logging, shutil, sys, tempfile
from pathlib import Path, PurePath

from PyPDF2 import PdfFileWriter, PdfFileReader, pdf
from bookleter import shuffle


class Book():
    def __init__(
        self,
        input_file_path,
        start_page_number,
        end_page_number,
        direction,
        crop,
        ):

        self._validate_inputs(
            input_file_path,
            start_page_number,
            end_page_number,
            crop
        )

        current_path = Path.cwd()
        self.input_file_path = PurePath.joinpath(current_path, input_file_path)
        self.start_page_number = int(start_page_number)
        self.end_page_number = int(end_page_number)
        self.direction = direction
        self.crop = crop


        logging.basicConfig(level=logging.NOTSET)
        
        self.temp_path = Path(tempfile.gettempdir())

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

        print_order = shuffle.foop(self.correct_pages_count)

        if self.direction == "rtl":
            logging.info("changing book direction to rtl...")
            self._reverse_pages_order()

            logging.info("shuffling pages order...\ncreating final pdf...")
            self._shuffle_pdf(self.reversed_blanked_shuffled_pdf_name, print_order)

            logging.info("cropping...")
            self._set_crop(self.reversed_blanked_shuffled_pdf_name, self.final_pdf_name)

        else:
            self._shuffle_pdf(self.blanked_shuffled_pdf_name, print_order)

            logging.info("cropping...")
            self._set_crop(self.blanked_shuffled_pdf_name, self.final_pdf_name)


        if self._get_pdf_pages_count(self.original_pdf_path) >= 8:
            logging.info("creating test pdf...")
            self._pickout_pages(1, 8)

            if self.direction == "rtl":
                self._reverse_pages_order()

            print_order = shuffle.foop(8)
            self._shuffle_pdf(self.reversed_blanked_shuffled_test_pdf_name, print_order)

            self._set_crop(self.reversed_blanked_shuffled_test_pdf_name, self.test_pdf_name)
        else:
            # a book with less than 8 pages doesn't need a test pdf file
            logging.info("skip creating test pdf...")

        logging.info("cleaning up...")
        # shutil.rmtree(self.temp_path)

        logging.info("finished!")

    def _get_pdf_pages_count(self, input_file_path):
        pdf = PdfFileReader(open(input_file_path, "rb"))
        return pdf.getNumPages()

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

    def _set_crop(self, input_pdf_name, output_pdf_name):

        inputpdf = PdfFileReader(open(input_pdf_name, "rb"))
        output = PdfFileWriter()

        for page in inputpdf.pages:
            page.cropBox.lowerLeft = tuple([a + b for a, b in zip(page.cropBox.lowerLeft, (int(self.crop['left']), int(self.crop['bottom'])))])
            page.cropBox.upperRight = tuple([a - b for a, b in zip(page.cropBox.upperRight, (int(self.crop['right']), int(self.crop['top'])))])
            
            output.addPage(page)
        with open(output_pdf_name, "wb") as output_stream:
            output.write(output_stream)

    def _validate_inputs(
            self,
            input_file_path,
            start_page_number,
            end_page_number,
            crop
        ):
        if input_file_path == "":
            raise ValueError('Please add a pdf file')
        
        if "" in (start_page_number, end_page_number):
            raise ValueError('Please enter start and end page numbers')
        else:
            try:
                int(start_page_number)
                int(end_page_number)
            except:
                raise ValueError('Start and end page value must be a number')
        
        if int(end_page_number) > self._get_pdf_pages_count(input_file_path):
            raise ValueError('End page number out of range\nYour book has only {} pages'.format(self._get_pdf_pages_count(input_file_path)))
        

        crop_values = ["" for key in crop.keys() if key == crop[key]]
        if "" in crop_values:
            raise ValueError('Please enter all the crop values')
        else:
            for val in crop.values():
                try:
                    int(val)
                except:
                    raise ValueError('Crop value must be a number')



    def __str__(self):
        return str({
            "pdf_file_path": self.input_file_path,
            "start_page": self.start_page_number,
            "end_page": self.end_page_number,
            "crop": self.crop,
            "book_direction": self.direction
        })