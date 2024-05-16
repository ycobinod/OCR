# pdf/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import PDFFile
from .pdf_processing import extract_text_and_images_from_pdf

def upload_pdf(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        pdf_file = PDFFile.objects.create(original_file=uploaded_file)
        output_path = f"media/processed_pdfs/{uploaded_file.name}"
        image_output_folder = "media/extracted_images"
        extract_text_and_images_from_pdf(pdf_file.original_file.path, output_path, image_output_folder)
        pdf_file.processed_file = output_path
        pdf_file.save()
        return JsonResponse({'message': 'File processed successfully', 'processed_file': pdf_file.processed_file.url})
    return render(request, 'upload.html')
