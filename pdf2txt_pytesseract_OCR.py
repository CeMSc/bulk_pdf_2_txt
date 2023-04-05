import os
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe" # Check validity
from PIL import Image

def pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ''
        for page_num in range(reader.numPages):
            page_text = reader.getPage(page_num).extractText()
            lines = page_text.split('\n')
            text += ' '.join(line if line.strip().endswith(('.', '?', '!')) else line.strip() for line in lines)
        return text

def ocr_pdf_to_text(pdf_path, lang='eng'):
    images = convert_from_path(pdf_path)
    text = ''
    for img in images:
        page_text = pytesseract.image_to_string(img, lang=lang)
        lines = page_text.split('\n')
        text += ' '.join(line if line.strip().endswith(('.', '?', '!')) else line.strip() for line in lines)
    return text

def save_text_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

def main():
    input_folder = 'PDF'
    output_folder = 'TXT'
 
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(input_folder, filename)
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(output_folder, txt_filename)

            try:
                text = pdf_to_text(pdf_path)
                if not text.strip():
                    text = ocr_pdf_to_text(pdf_path, lang='eng')
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue

            save_text_file(text, txt_path)
            print(f"Converted {filename} to {txt_filename}")

if __name__ == '__main__':
    main()
