from django.db import models

class PDFFile(models.Model):
    original_file = models.FileField(upload_to='original_pdfs/')
    processed_file = models.FileField(upload_to='processed_pdfs/', null=True, blank=True)