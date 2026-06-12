from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
import os


class ShareForm(forms.Form):
    file = forms.FileField()
    sender_email = forms.EmailField()
    recipient_email = forms.EmailField()

    def clean_file(self):
        f = self.cleaned_data.get('file')
        if not f:
            raise ValidationError('No file provided.')
        max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 50 * 1024 * 1024)
        if f.size > max_size:
            raise ValidationError(f'File is too large (max {max_size // (1024*1024)} MB).')
        ext = os.path.splitext(f.name)[1].lower()
        allowed = getattr(settings, 'ALLOWED_UPLOAD_EXTENSIONS', None)
        if allowed and ext not in allowed:
            raise ValidationError(f'Files of type {ext} are not allowed. Allowed: {", ".join(allowed)}')
        return f


class DeclineForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
