from django.contrib import admin
from .models import UploadedFile, ShareLink


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('original_name', 'uploaded_at')


@admin.register(ShareLink)
class ShareLinkAdmin(admin.ModelAdmin):
    list_display = ('token', 'file', 'sender_email', 'recipient_email', 'created_at', 'expires_at', 'claimed', 'expired')
    readonly_fields = ('token', 'created_at')
