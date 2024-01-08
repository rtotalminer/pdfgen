import json
from lxml import html

import tesserocr
from bs4 import BeautifulSoup
from PIL import Image

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch

DATA_PATH = r'C:\Users\Robert'

image_path = '../data/sample/readbale_book_en-20.png'
with tesserocr.PyTessBaseAPI(lang="eng", path=rf'{DATA_PATH}\tessdata') as api:
    image = Image.open(image_path)
    api.SetImage(image)
    hocr_text = api.GetHOCRText(0)

soup = BeautifulSoup(hocr_text, 'html.parser')
page = soup.find('div', class_='ocr_page').get('title').split(';')
bbox = [int(value) for value in page[1].split(' ')[2:6]]

lines = [] # line or paragraph is the question
for _line in soup.find_all('span', class_='ocr_line'):
    title = _line.get('title').split(';')
    lines.append({
        'bbox': [int(value) for value in title[0].split(' ')[1:5]],
        'baseline': [float(value) for value in title[1].split(' ')[2:4]],
        'x_size': float(title[2].split(' ')[2]),
        'x_descenders': float(title[3].split(' ')[2]),
        'x_ascenders': float(title[4].split(' ')[2]),
        'words': [word.text for word in _line.find_all('span', class_='ocrx_word')]
    })


pdf_path = "../output.pdf"
pdf = canvas.Canvas(pdf_path)

pdf.setPageSize((bbox[2], bbox[3]))
print(((bbox[2], bbox[3])))

def draw_bbox(pdf, _bbox, color="red", width=2):
    pdf.setStrokeColor(colors.red)
    pdf.setLineWidth(width)
    pdf.rect(_bbox[0], bbox[3] - _bbox[3], _bbox[2] - _bbox[0], _bbox[3] - _bbox[1])

# Draw the bbox for the OCR page
draw_bbox(pdf, bbox)

# draw each line.
for line in lines:
    font_size = line['x_size']
    words = ' '.join(line["words"])
    pdf.setFont("Helvetica", int(font_size))
    pdf.drawCentredString(
        line['bbox'][0] + (line['bbox'][2] - line['bbox'][0]) / 2,
        bbox[3] - line['bbox'][3] - (line['bbox'][3] - line['bbox'][1]) / 2,
        str(words)
    )

# Save the PDF
pdf.save()





































# data = {
#     'bbox': [],
#     'lines': [],
#     'photos': []
# }

# pdf_path = "output.pdf"
# pdf = canvas.Canvas(pdf_path, pagesize=letter)

# x, y = data['bbox'][2], data['bbox'][3]
# pdf.setPageSize((x, y))

# def draw_bbox(pdf, bbox, color="red", width=2):
#     pdf.setStrokeColor(colors.red)
#     pdf.setLineWidth(width)
#     pdf.rect(bbox[0], y - bbox[3], bbox[2] - bbox[0], bbox[3] - bbox[1])

# # Draw the bbox for the OCR page
# draw_bbox(pdf, data["bbox"])

# # draw each line.


# # Draw the bbox for each carea
# for carea in metadata["careas"]:

#     for para in carea["pars"]:

#         for line in para['lines']:
#             font_size = line['x_size']
#             words = []
            
#             # Draw the bbox for each word
#             for word in line["words"]:
#                 words.append(word['word'])
#             print(words)
#             word = ' '.join(words)
#             pdf.setFont("Helvetica", int(font_size))
#             pdf.drawCentredString(line['bbox'][0] + (line['bbox'][2] - line['bbox'][0]) / 2,
#                                   y - line['bbox'][3] - (line['bbox'][3] - line['bbox'][1]) / 2,
#                                   str(word))

# for photo in metadata["photos"]:
#     draw_bbox(pdf, photo["bbox"])

# # Save the PDF
# pdf.save()

# print('PDF Created!')

## fIrst thing to do to noramloise the data is to
## append each word to the line and print the line instead