import os
import fitz
import pytesseract
from PIL import Image
from io import BytesIO
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PDFFile

@csrf_exempt
def upload_pdf(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        uploaded_file = request.FILES['file']
        pdf_file = PDFFile.objects.create(original_file=uploaded_file)
        
        # Process the PDF and keep it in memory instead of saving it
        output = BytesIO()
        image_output_folder = "media/extracted_images"
        process_pdf(uploaded_file, output, image_output_folder)
        
        response = HttpResponse(output.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{uploaded_file.name}"'
        
        return response
    return JsonResponse({'error': 'Invalid request'}, status=400)

def process_pdf(uploaded_file, output, image_output_folder):
    try:
        if not os.path.exists(image_output_folder):
            os.makedirs(image_output_folder)

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
                image_path = os.path.join(image_output_folder, f"page_{page_index}_image_{image_index}.png")
                
                # Save the image and verify its path
                image.save(image_path)
                print(f"Saved image: {image_path}")
                
                textbox = fitz.Rect(0, 0, image_width, image_height)
                page.insert_textbox(textbox, text)
        
        doc.save(output)
        doc.close()
        print("Processed PDF in memory.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
