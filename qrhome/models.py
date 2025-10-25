from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Extend the built-in User model to store mobile number (required for your project)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    def __str__(self):
        return self.user.username + f" ({self.mobile_number})"

# Model to track generated QR codes
class QRCodeHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Input fields
    data_content = models.TextField(verbose_name="Text/Link Used")
    prompt_used = models.TextField(verbose_name="AI Prompt", blank=True, null=True)
    
    # Output fields
    # NOTE: In a production app, you'd use FileField/ImageField, but CharField
    # is simpler for this PWP to store the base64/URL of the QR code image.
    qr_code_path = models.CharField(max_length=255, verbose_name="QR Code Image Path/Base64")
    
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "QR Code Histories"
        ordering = ['-generated_at']

    def __str__(self):
        return f"QR for {self.user.username} on {self.generated_at.strftime('%Y-%m-%d %H:%M')}"