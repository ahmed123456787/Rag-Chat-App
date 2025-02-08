from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ['file', 'uploaded_at','message']
        read_only_fields = ['uploaded_at']
        
    def validate_document(self, value):
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("The document must be a PDF file.")
        return value

    def create(self, validated_data):
        return super().create(validated_data)
        
