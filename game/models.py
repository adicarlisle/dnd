import mimetypes
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# 📏 Custom validator for background assets (Maps/Scenes - Up to 25MB)
def validate_background_media(file):
    max_size_mb = 25
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Background assets cannot exceed {max_size_mb}MB.")
    
    # Check that the file falls into either image or video categories
    mime_type, _ = mimetypes.guess_type(file.name)
    if mime_type:
        if not (mime_type.startswith('image/') or mime_type.startswith('video/')):
            raise ValidationError("Unsupported file format! Please upload a valid image or video file.")
    else:
        raise ValidationError("Could not verify file type. Ensure it has a standard extension.")

# 📏 Custom validator for player token assets (Tokens/Actions - Up to 10MB)
def validate_token_media(file):
    max_size_mb = 10
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Character tokens/clips cannot exceed {max_size_mb}MB.")
        
    mime_type, _ = mimetypes.guess_type(file.name)
    if mime_type:
        if not (mime_type.startswith('image/') or mime_type.startswith('video/')):
            raise ValidationError("Unsupported file format! Please upload a valid image or video file.")
    else:
        raise ValidationError("Could not verify file type. Ensure it has a standard extension.")


class BackgroundAsset(models.Model):
    title = models.CharField(max_length=100)
    # Changed to FileField to allow video formats seamlessly
    image = models.FileField(upload_to='backgrounds/', validators=[validate_background_media])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PlayerPost(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending DM Review'),
        ('APPROVED', 'Merged into Dashboard'),
        ('REJECTED', 'Rejected'),
    ]
    
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    # Changed to FileField to allow video/animated clips seamlessly
    character_token = models.FileField(upload_to='player_tokens/', blank=True, null=True, validators=[validate_token_media])
    selected_background = models.ForeignKey(BackgroundAsset, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.username} - {self.status}"