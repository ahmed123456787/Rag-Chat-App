from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView
from .serializers import DocumentUploadSerializer
from rest_framework.response import Response

class DocumentUploadView(GenericAPIView, CreateModelMixin):
    """View for uploading a document."""
    serializer_class = DocumentUploadSerializer

    def post(self, request):
        
        return self.create(request)



class TestView(GenericAPIView):
    """View for testing."""
    def get(self, request):
        return Response({'message': 'Hello, world!'})