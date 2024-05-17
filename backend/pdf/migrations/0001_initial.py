# Generated by Django 4.2.2 on 2024-05-17 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PDFFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_file', models.FileField(upload_to='original_pdfs/')),
                ('processed_file', models.FileField(blank=True, null=True, upload_to='processed_pdfs/')),
            ],
        ),
    ]
