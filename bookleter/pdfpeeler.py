#!/usr/bin/env python

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
    Credits
    This part of the application uses an Open Source component.
    You can find the source code of the open source project along with license information below.
    i am grateful to this developer for his/her contribution to open source.

    Project: (pdfpeeler) https://github.com/hitzg/pdfpeeler
    License (GNU General Public License v3.0) https://www.gnu.org/licenses/gpl-3.0.en.html 
"""

import os
import subprocess
import itertools
import argparse

# seems that there are two forks of pypdf. 
try:
    import PyPDF2 as pdf
except ImportError:
    try:
        import pyPdf as pdf
        print("PyPDF2 is not installed. Falling back to pyPdf.")
    except ImportError:
        raise ImportError("Neither pyPdf nor PyPDF2 are installed")


# conversion factors 
mm_per_inch = 25.4
dpi = 72.

def get_output_filename(infile, prefix = "", suffix = "", extension=None):
    path, fname = os.path.split(infile)
    fname, ext = os.path.splitext(fname)
    if extension is not None:
        ext = extension
    ext = ext.strip('. ')
    return os.path.join(path, '{}{}{}.{}'.format(prefix, fname, suffix, ext))


def get_bounding_boxes(pdffile, resolution=72, verbose=False):
    """ calls ghost script to retrieve the bounding boxes of all pages of the
    provided pdf file 

    Parameters
    ----------
    pdffile: str
        Path to the input pdf file
    resolution: int, optional
        The desired resolution at which the pdf is rendered (Default: 72)
    verbose: bool, optional
        Be verbose. (Default: False)

    Returns
    -------
    list
        Returns a list of lists with one entry per page of the following
        format: [lower_left_x, lower_left_y, upper_right_x, upper_right_y,
                width, height]
    """
    
    command = ['gs', '-dBATCH', '-dNOPAUSE', '-sDEVICE=bbox',
            '-r' + str(resolution), pdffile]
    subp = subprocess.Popen(command, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    stdout, stderr = subp.communicate()

    # some output if requested
    if verbose:
        print ("Ghost script:")
        print (" command: {}".format(' '.join(command)))
        print (" output:")
        for line in stdout.split('\n'):
            print ("   {}".format(line))

    if subp.returncode:
        raise EnvironmentError("'gs' call failed.")
    bboxes = [list(map(float, s.split()[1:])) for s in stderr.decode('utf-8', errors='ignore').split('\n') if
            s.startswith(r'%%HiResBoundingBox:')]

    # add width and height to the bounding boxes (this is redundant, but
    # convenient)
    bboxes = [bb + [bb[2]-bb[0], bb[3] - bb[1]] for bb in bboxes]
    return bboxes


def peel_pdf(infile, outfile, uniform_page_size=True, margins=None,
        resolution=72, verbose=False):
    
    # get the bounding boxes of each page
    bboxes = get_bounding_boxes(infile, resolution=resolution, verbose=verbose)

    # output them if we are verbose
    if verbose:
        print ("Extracted bounding boxes:")
        for n,b in enumerate(bboxes):
            print ("   page {: 3d}: " + "".join(["{: 8.1f}"]*6)) .format(n, *b)

    # instantiate pdf objects
    input_pdf = pdf.PdfFileReader(open(infile, "rb"))
    output_pdf = pdf.PdfFileWriter()
    num_pages = input_pdf.getNumPages()

    if uniform_page_size:
        # First we get the max width and height, then replace all the heights
        # and widths for each page with leftlower + width/height, respectively.
        mb =  map(max, zip(*bboxes)[4:])
        bboxes = [[bb[0], bb[1], bb[0] + mb[0], bb[1] + mb[1], mb[0], mb[1]] 
                for bb in bboxes]
        if verbose:
            print ("Using global width and height: {:.1f}, {:.1f}".format(*mb))
        
    if margins is None:
        margins = [0,0,0,0]

    # iterate over the pages 
    for i, bb in zip(range(num_pages), bboxes):
        
        # get the page and its mediabox
        page = input_pdf.getPage(i)
        media_box = page.mediaBox

        # get the lower left point of the current page
        ll_x = float(media_box.getLowerLeft_x())
        ll_y = float(media_box.getLowerLeft_y())

        # make sure that the lower left corner of the page is low enough to fit
        # the entire height of the input page onto the output page (this is
        # only relevant for the uniform page size case)
        # NOTE: I'm not sure if this makes sense for the y direction
        x_off = max(0, ll_x + bb[2] - float(media_box[2]))
        y_off = max(0, ll_y + bb[3] - float(media_box[3]))
        
        # assign the new media box size
        page.mediaBox.lowerLeft = [bb[0] + ll_x - x_off - margins[0], bb[1] +
                ll_y - y_off - margins[1]]
        page.mediaBox.upperRight = [bb[2] + ll_x - x_off + margins[2],  bb[3] +
                ll_y - y_off + margins[3]]

        # add the modified page to the output doc
        output_pdf.addPage(page)
    
    # write the output file
    output_stream = open(outfile, "wb")
    output_pdf.write(output_stream)
    output_stream.close()

def peeler_main():
    def margin_checker(margins):
        """ helper function to parse the margin arguments """
        try:
            value =  float(margins)
            return [value]*4
        except ValueError:
            try:
                splits = margins.split(',')
                assert len(splits)==4
                return map(float, splits)
            except (ValueError, AssertionError):
                msg = "'%s' is not a proper margin specification" % margins
                raise argparse.ArgumentTypeError(msg)

    parser = argparse.ArgumentParser(
            description='Peel those large margins off your pdfs')
    parser.add_argument('files', metavar='infile', type=str, nargs='+',
            help='Input files to be processed')
    parser.add_argument('-p', '--page-wise', dest='pagewise',
            action='store_true', help='Process each page individually')
    parser.add_argument('-i', '--inches', dest='inches', action='store_true',
            help='Margins are specified in inches otherwise in mm')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
            help='Be verbose')
    parser.add_argument('-m', '--margins', dest='margins', action='store',
            type=margin_checker, help='Extra margins to add. Either this is ' \
            'a float, or a comma separated list of 4 floats (left, bottom, ' \
            'right, top)')
    parser.add_argument('-o', '--output-file', dest='outfile', action='store',
            default=None, help='The output filename. This is only applicable' \
            ' if only one input file is specified')
    
    args = parser.parse_args()
    if len(args.files) > 1 and args.outfile is not None:
        msg = "this can only be specified for one input file"
        raise argparse.ArgumentError(args.outfile, msg)

    for f in args.files:
        outfile = args.outfile
        if args.outfile is None:
            outfile = get_output_filename(f, suffix='_peeled')
        
        margins = None
        if args.margins is not None:
            if args.inches:
                margins = [m*dpi for m in args.margins]
            else:
                margins  = [m*dpi/mm_per_inch for m in args.margins]
        peel_pdf(f, outfile, uniform_page_size=not args.pagewise,
                margins=margins, resolution=dpi, verbose=args.verbose)

if __name__ == '__main__':
    peeler_main()
    
    




