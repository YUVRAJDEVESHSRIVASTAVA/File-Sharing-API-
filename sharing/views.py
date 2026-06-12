from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from urllib.parse import urljoin

from .forms import ShareForm, DeclineForm
from .models import UploadedFile, ShareLink


def index(request):
    if request.method == 'POST':
        form = ShareForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['file']
            sender = form.cleaned_data['sender_email']
            recipient = form.cleaned_data['recipient_email']

            uploaded = UploadedFile.objects.create(file=f, original_name=f.name)

            expires = timezone.now() + timedelta(minutes=30)
            share = ShareLink.objects.create(
                file=uploaded,
                sender_email=sender,
                recipient_email=recipient,
                expires_at=expires,
            )

            claim_path = reverse('sharing:claim', args=[share.token])
            site_url = getattr(settings, 'SITE_URL', None)
            if site_url:
                claim_url = urljoin(site_url, claim_path)
            else:
                claim_url = request.build_absolute_uri(claim_path)
            subject = 'A file was shared with you'
            message = f"{sender} shared a file with you: {uploaded.original_name}\n\nClaim it here: {claim_url}\n\nThis link will expire in 30 minutes."
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])

            return redirect('sharing:share_done', token=share.token)
    else:
        form = ShareForm()
    return render(request, 'sharing/index.html', {'form': form})


def share_done(request, token):
    share = get_object_or_404(ShareLink, token=token)
    claim_path = reverse('sharing:claim', args=[share.token])
    site_url = getattr(settings, 'SITE_URL', None)
    if site_url:
        link = urljoin(site_url, claim_path)
    else:
        link = request.build_absolute_uri(claim_path)
    return render(request, 'sharing/share_done.html', {'share': share, 'link': link})


def claim_view(request, token):
    share = get_object_or_404(ShareLink, token=token)
    if share.expired or share.is_expired():
        return render(request, 'sharing/expired.html', {'share': share})

    if request.method == 'POST':
        if not share.claimed:
            share.claimed = True
            share.claimed_at = timezone.now()
            share.save()
            # notify sender that file was claimed
            subject = 'Your file was claimed'
            message = f"Your file '{share.file.original_name}' was claimed by {share.recipient_email} at {share.claimed_at}."
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [share.sender_email])
        return redirect('sharing:download', token=share.token)

    return render(request, 'sharing/claim.html', {'share': share})


def download_view(request, token):
    share = get_object_or_404(ShareLink, token=token)
    if not share.claimed:
        return redirect('sharing:claim', token=token)

    uploaded = share.file
    uploaded.file.open('rb')
    response = FileResponse(uploaded.file, as_attachment=True, filename=uploaded.original_name)
    return response


def decline_view(request, token):
    share = get_object_or_404(ShareLink, token=token)
    if request.method == 'POST':
        form = DeclineForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data.get('reason')
            share.declined = True
            share.decline_reason = reason
            share.save()
            # notify sender immediately
            subject = 'Recipient declined your shared file'
            message = f"Your file '{share.file.original_name}' was declined by {share.recipient_email}. Reason: {reason or 'No reason provided.'}"
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [share.sender_email])
            return render(request, 'sharing/decline_done.html', {'share': share})
    else:
        form = DeclineForm()
    return render(request, 'sharing/decline.html', {'form': form, 'share': share})
