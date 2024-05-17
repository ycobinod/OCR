from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from pdf import views

urlpatterns = [
    path('upload/', views.upload_pdf, name='upload_pdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
