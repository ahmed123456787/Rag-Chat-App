from django.urls import path, include
from .views import DocumentUploadView, TestView 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('document/', DocumentUploadView.as_view(), name='document'),
    path('test/',TestView.as_view(), name='test'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)