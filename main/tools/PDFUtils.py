from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTImage
from io import StringIO


# https://www.cnblogs.com/wj-1314/p/9429816.html

class PDFUtils:

    def __init__(self):
        pass

    def pdf2pages(self, path):
        with open(path, 'rb') as f:
            output = StringIO()
            praser = PDFParser(f)

            doc = PDFDocument(praser)

            if not doc.is_extractable:
                raise PDFTextExtractionNotAllowed

            pdfrm = PDFResourceManager()

            laparams = LAParams()

            device = PDFPageAggregator(pdfrm, laparams=laparams)

            interpreter = PDFPageInterpreter(pdfrm, device)

            pages = []
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
                layout = device.get_result()
                pages.append(layout)
            # for x in layout:
            #     if hasattr(x, "get_text"):
            #         content = x.get_text()
            #         output.write(content)

            # content = output.getvalue()
            output.close()
            # return content
            return pages
