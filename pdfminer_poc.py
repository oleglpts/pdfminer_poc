#!/usr/bin/python3

import os
import sys
import shutil
import argparse


if __name__ == '__main__':
    #
    # Documents: https: // buildmedia.readthedocs.org / media / pdf / pdfminer - docs / latest / pdfminer - docs.pdf
    #
    sys.path.append('../')
    from utils import virtual_environment
    parser = argparse.ArgumentParser(prog='pdfminer.poc')
    parser.add_argument('file_name', type=str)
    cmd_args = virtual_environment(parser)
    from pdfminer3.pdfdocument import PDFDocument
    from pdfminer3.pdftypes import PDFObjectNotFound
    from pdfminer3.pdfparser import PDFParser, PDFStream
    print(cmd_args.file_name)
    input_file = open(cmd_args.file_name, "rb")
    parsed = PDFDocument(PDFParser(input_file))
    try:
        shutil.rmtree('%s.pdfminer_out' % cmd_args.file_name)
    except FileNotFoundError:
        pass
    os.mkdir('%s.pdfminer_out' % cmd_args.file_name)
    for obj_id in set(obj_id for xref in parsed.xrefs for obj_id in xref.get_objids()):
        try:
            obj = parsed.getobj(obj_id)
        except PDFObjectNotFound:
            continue
        if not isinstance(obj, PDFStream):
            continue
        print('%s' % obj)
        obj.decode()
        length = obj.attrs.get('Length', '')
        output_file = open('%s.pdfminer_out/pdf_%04d_0.dat' % (cmd_args.file_name, obj_id), 'wb')
        output_file.write(obj.data)
        output_file.close()
