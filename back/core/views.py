import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .serializers import DocumentSerializer


# Call the RAG module
from .rag.main import init

class DocumentUploadView(APIView):
    """View for uploading a document without saving it in a model."""

    def post(self, request, *args, **kwargs):
       
        serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        file_path = os.path.join(settings.MEDIA_ROOT, "documents", file.name)


        # Check if file already exists
        if os.path.exists(file_path):
            file_url = request.build_absolute_uri(settings.MEDIA_URL + "documents/" + file.name)
        else:   
            saved_path = default_storage.save("documents/" + file.name, ContentFile(file.read()))
            file_url = request.build_absolute_uri(settings.MEDIA_URL + saved_path)

        # Call the RAG module
        extracted_texts = init(file.name,request.data['message'])
        print(extracted_texts)
        return Response({
            "message": extracted_texts,
            "file_url": file_url
        }, status=status.HTTP_201_CREATED)
#  return Response({
#                 "message": "File already exists.",
#                 "file_url": file_url
#             }, status=status.HTTP_200_OK)


class TestView(APIView):
    """View for testing."""
    
    def get(self, request):
        return Response({'message': 'Hello, world!'})
