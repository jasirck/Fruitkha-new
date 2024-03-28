from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("sales_report", views.sales_report, name="sales_report"),
    path("generate_pdf", views.generate_pdf, name="generate_pdf"),
    path("generate_excel", views.generate_excel, name="generate_excel"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
