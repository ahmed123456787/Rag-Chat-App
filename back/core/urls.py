from django.urls import path
from .views import DocumentUploadView, TestView 

urlpatterns = [
    path('document/', DocumentUploadView.as_view(), name='document-upload'),
    path('test/',TestView.as_view(), name='test'),
]