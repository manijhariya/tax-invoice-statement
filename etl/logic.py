# from invoice2data import extract_data
# from invoice2data.extract.loader import read_templates


# def extract_da(filename : str):
#     templates = read_templates('./')
#     print(templates)
#     result = extract_data(filename, templates=templates)
#     print(result)


ex_pdf= '/home/alan/Downloads/Test PDF.pdf'

# extract_da(ex_pdf)
import io
from PyPDF2 import PdfReader

reader = PdfReader(ex_pdf)
page = reader.pages[0]
extracted_text = page.extract_text()
for line in io.StringIO(extracted_text):
    print(line)
