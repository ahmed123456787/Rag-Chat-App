from rest_framework import serializers

class DocumentUploadSerializer(serializers.Serializer):
    document = serializers.FileField()

    def validate_document(self, value):
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("The document must be a PDF file.")
        return value

    class Meta:
        fields = ['document']