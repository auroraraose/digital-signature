from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who uploaded the document
    original_pdf = models.FileField(upload_to='documents/original_pdfs/')  # Stores the uploaded PDF file
    signed_pdf = models.FileField(upload_to='documents/signed_pdfs/', null=True, blank=True)  # Stores the signed PDF (null initially)
    uploaded_at = models.DateTimeField(default=timezone.now)  # Track when the document was uploaded
    signed_at = models.DateTimeField(null=True, blank=True)  # Track when the document was signed
    signature_status = models.CharField(
        max_length=20, choices=[('pending', 'Pending'), ('signed', 'Signed')],
        default='pending'
    )  # Indicates whether the document has been signed or not

    def __str__(self):
        return f"Document {self.id} by {self.user.username}"
