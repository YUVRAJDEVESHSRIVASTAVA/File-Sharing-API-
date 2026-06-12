from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction

from sharing.models import ShareLink


class Command(BaseCommand):
    help = 'Expire unclaimed share links, notify senders, and clean up files'

    def handle(self, *args, **options):
        now = timezone.now()
        expired_qs = ShareLink.objects.filter(claimed=False, expires_at__lte=now)
        count = expired_qs.count()
        processed = 0
        for link in expired_qs:
            # capture file object and related info before deletion
            file_obj = link.file
            recipient = link.recipient_email
            sender = link.sender_email
            reason = link.decline_reason or 'No reason provided by recipient.'
            subject = 'Shared file not claimed'
            message = (
                f"Hello,\n\n"
                f"Your shared file '{file_obj.original_name}' sent to {recipient} was not claimed within 30 minutes.\n\n"
                f"Recipient: {recipient}\n"
                f"Reason: {reason}\n\n"
                f"The share link has been removed to protect your file.\n"
                f"If you want to share the file again, please upload and share it from the app.\n\n"
                f"Regards,\nFileShare"
            )
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [sender])
            except Exception as e:
                self.stderr.write(f"Failed to send notification for link {link.token}: {e}")

            # Determine if other links reference this uploaded file
            other_links = file_obj.share_links.exclude(pk=link.pk).count()

            # Delete the share link and clean up the uploaded file if unused
            try:
                with transaction.atomic():
                    link.delete()
                    if other_links == 0:
                        try:
                            file_obj.file.delete(save=False)
                        except Exception as e:
                            self.stderr.write(f"Failed to delete file content for {file_obj}: {e}")
                        try:
                            file_obj.delete()
                        except Exception as e:
                            self.stderr.write(f"Failed to delete UploadedFile record {file_obj}: {e}")
            except Exception as e:
                self.stderr.write(f"Failed to delete link {link.token}: {e}")

            processed += 1

        self.stdout.write(self.style.SUCCESS(f'Processed {processed} expired links'))
