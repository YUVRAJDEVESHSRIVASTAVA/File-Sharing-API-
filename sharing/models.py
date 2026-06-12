from django.db import models
from django.utils import timezone
from datetime import timedelta
import secrets


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    original_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name


class ShareLink(models.Model):
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='share_links')
    token = models.CharField(max_length=128, unique=True, db_index=True)
    sender_email = models.EmailField()
    recipient_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    claimed = models.BooleanField(default=False)
    claimed_at = models.DateTimeField(null=True, blank=True)
    declined = models.BooleanField(default=False)
    decline_reason = models.TextField(null=True, blank=True)
    expired = models.BooleanField(default=False)
    notified_sender = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(16)
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=30)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"ShareLink {self.token} -> {self.recipient_email}"
