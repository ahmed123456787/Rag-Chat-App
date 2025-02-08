from django.db import models


class Document(models.Model):
    file = models.FileField(unique=True, upload_to='documents/')  # Uploads files to 'media/documents/'
    message = models.TextField(blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.file.name
