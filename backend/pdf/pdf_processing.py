import os
import fitz
import pytesseract
from PIL import Image
from io import BytesIO

def extract_text_from_pdf(pdf_path, output_path):
    try:
        doc = fitz.open(pdf_path)
        for page_index in range(len(doc)):
            page = doc[page_index]
            image_list = page.get_images()
            if not image_list:
                continue
            for image_index, img in enumerate(page.get_images(), start=1):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(BytesIO(image_bytes))
                text = pytesseract.image_to_string(image)
                image_width = base_image["width"]
                image_height = base_image["height"]
                page.delete_image(xref)
                
                textbox = fitz.Rect(0, 0, image_width, image_height)
                page.insert_textbox(textbox, text)
        
        doc.save(output_path)
        doc.close()
        print(f"Processed PDF saved: {output_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
