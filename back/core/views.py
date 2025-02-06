from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView
from .serializers import DocumentUploadSerializer

class DocumentUploadView(GenericAPIView, CreateModelMixin):
    """View for uploading a document."""
    serializer_class = DocumentUploadSerializer

    def post(self, request):
        
        return self.create(request)

