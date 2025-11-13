from django.conf import settings
from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Profile

from .models import Profile

signer = TimestampSigner()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_and_send_email(sender, instance, created, **kwargs):
    """
    Triggered when a user is created.
    - Creates a Profile.
    - Sends verification email with a 24-hour deletion link.
    """
    if created:
        # 1️⃣ Create the profile (safe even if mail fails)
        Profile.objects.get_or_create(user=instance)

        # 2️⃣ Generate a signed token for deletion link
        token = signer.sign(instance.pk)  # securely signs user ID with timestamp

        # 3️⃣ Build delete URL
        delete_url = f"http://127.0.0.1:8000/api/delete-account/?token={token}"

        # 4️⃣ Send confirmation mail
        try:
            send_mail(
                subject="Welcome to Our Instagram App 🎉",
                message=(
                    f"Hi {instance.username},\n\n"
                    f"Your account has been created successfully.\n"
                    f"If you did NOT create this account, click below to delete it:\n"
                    f"{delete_url}\n\n"
                    f"This link is valid for 24 hours."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=False,
            )
        except Exception as e:
            # Even if mail sending fails, the profile remains
            print(f"⚠️ Failed to send welcome email: {e}")
