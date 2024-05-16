from django.db import models

class PDFFile(models.Model):
    original_file = models.FileField(upload_to='pdfs/')
    processed_file = models.FileField(upload_to='processed_pdfs/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
