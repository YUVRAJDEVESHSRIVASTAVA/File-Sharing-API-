from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.core import mail

from sharing.forms import ShareForm
from sharing.models import UploadedFile, ShareLink


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend', DEFAULT_FROM_EMAIL='no-reply@fileshare.local')
class ValidationTests(TestCase):
    def test_file_too_large(self):
        # set a tiny MAX_UPLOAD_SIZE
        with override_settings(MAX_UPLOAD_SIZE=10):
            content = b'x' * 20
            f = SimpleUploadedFile('big.txt', content)
            form = ShareForm(data={'sender_email': 's@example.com', 'recipient_email': 'r@example.com'}, files={'file': f})
            self.assertFalse(form.is_valid())
            self.assertIn('file', form.errors)

    def test_disallowed_extension(self):
        with override_settings(ALLOWED_UPLOAD_EXTENSIONS=['.txt']):
            f = SimpleUploadedFile('bad.exe', b'ok')
            form = ShareForm(data={'sender_email': 's@example.com', 'recipient_email': 'r@example.com'}, files={'file': f})
            self.assertFalse(form.is_valid())
            self.assertIn('file', form.errors)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend', DEFAULT_FROM_EMAIL='no-reply@fileshare.local')
class ExpireLinksTests(TestCase):
    def test_expire_link_removes_share_and_file(self):
        f = SimpleUploadedFile('doc.txt', b'content')
        uploaded = UploadedFile.objects.create(file=f, original_name='doc.txt')
        expires = timezone.now() - timedelta(minutes=1)
        link = ShareLink.objects.create(file=uploaded, sender_email='sender@example.com', recipient_email='recip@example.com', expires_at=expires)

        call_command('expire_links')

        # link should be removed and sender notified
        self.assertFalse(ShareLink.objects.filter(pk=link.pk).exists())
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('not claimed', mail.outbox[0].subject.lower())

        # UploadedFile should be removed because no other links
        self.assertFalse(UploadedFile.objects.filter(pk=uploaded.pk).exists())

    def test_expire_link_keeps_file_if_other_links(self):
        f = SimpleUploadedFile('doc2.txt', b'hello')
        uploaded = UploadedFile.objects.create(file=f, original_name='doc2.txt')
        expired = ShareLink.objects.create(file=uploaded, sender_email='s1@example.com', recipient_email='r1@example.com', expires_at=timezone.now() - timedelta(minutes=1))
        active = ShareLink.objects.create(file=uploaded, sender_email='s2@example.com', recipient_email='r2@example.com', expires_at=timezone.now() + timedelta(minutes=30))

        call_command('expire_links')

        self.assertFalse(ShareLink.objects.filter(pk=expired.pk).exists())
        # active link remains
        self.assertTrue(ShareLink.objects.filter(pk=active.pk).exists())
        # uploaded file should still exist
        self.assertTrue(UploadedFile.objects.filter(pk=uploaded.pk).exists())


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend', DEFAULT_FROM_EMAIL='no-reply@fileshare.local')
class IntegrationE2ETests(TestCase):
    def test_share_and_claim_flow(self):
        f = SimpleUploadedFile('hello.txt', b'hello world')
        resp = self.client.post(reverse('sharing:index'), {'file': f, 'sender_email': 'me@example.com', 'recipient_email': 'you@example.com'})

        # share link created and initial email sent to recipient
        link = ShareLink.objects.first()
        self.assertIsNotNone(link)
        self.assertEqual(len(mail.outbox), 1)

        # recipient posts to claim (no GET to avoid template rendering in tests)
        claim_url = reverse('sharing:claim', args=[link.token])
        resp = self.client.post(claim_url)
        link.refresh_from_db()
        self.assertTrue(link.claimed)

        # claim sends notification to sender
        self.assertEqual(len(mail.outbox), 2)
