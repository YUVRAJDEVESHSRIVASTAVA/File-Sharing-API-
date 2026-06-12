from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from sharing.models import ShareLink


class Command(BaseCommand):
    help = 'Expire unclaimed share links and notify senders'

    def handle(self, *args, **options):
        now = timezone.now()
        expired = ShareLink.objects.filter(claimed=False, expired=False, expires_at__lte=now)
        count = expired.count()
        for link in expired:
            reason = link.decline_reason or 'No reason provided by recipient.'
            message = (
                f"Your shared file '{link.file.original_name}' was not claimed within 30 minutes."
                f"\n\nRecipient: {link.recipient_email}\nReason: {reason}"
            )
            send_mail('Shared file not claimed', message, settings.DEFAULT_FROM_EMAIL, [link.sender_email])
            link.expired = True
            link.notified_sender = True
            link.save()
        self.stdout.write(self.style.SUCCESS(f'Processed {count} expired links'))
