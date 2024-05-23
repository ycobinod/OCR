import os
import fitz
import pytesseract
from PIL import Image
from io import BytesIO
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from .models import PDFFile

@csrf_exempt
def upload_pdf(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        
        uploaded_file = request.FILES['file']
        pdf_file = PDFFile(original_file=uploaded_file)
        pdf_file.save()

        # Process the PDF 
        output = BytesIO()
        process_pdf(uploaded_file, output)

        # Save processed PDF to processed_file field
        processed_pdf_data = output.getvalue()
        pdf_file.processed_file.save(f'processed_{uploaded_file.name}.pdf', ContentFile(processed_pdf_data))

        response = HttpResponse(processed_pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="processed_{uploaded_file.name}"'

        return response
    return JsonResponse({'error': 'Invalid request'}, status=400)

def process_pdf(uploaded_file, output):
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
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
        
        doc.save(output)
        doc.close()
        print("Processed PDF in memory.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
