from io import BytesIO
import pdfreader
from pdfreader import PDFDocument, SimplePDFViewer

file_name = 'C:\\sai\\dev\\temp\\pdf\\tmobile\\SummaryBillApr2020.pdf'
# with open(file_name, "rb") as f:
#     stream = BytesIO(f.read())

# doc = PDFDocument(stream)
# page = next(doc.pages())
# print(page.Contents)
fd = open(file_name, "rb")
viewer = SimplePDFViewer(fd)
viewer.render()
date_string = viewer.canvas.strings[2] + viewer.canvas.strings[3]
print(date_string)
