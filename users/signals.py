from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Profile

User = get_user_model()
signer = TimestampSigner()


@receiver(post_save, sender=User)
def create_profile_and_send_email(sender, instance, created, **kwargs):
    if not created:
        return

    # ✅ Create profile safely
    Profile.objects.get_or_create(user=instance)

    # ✅ Generate signed token
    token = signer.sign(instance.pk)

    delete_url = f"http://127.0.0.1:8000/users/delete-account/?token={token}"
    print("🔥 SIGNAL FIRED")
    print("Delete URL:", delete_url)

    # OPTIONAL: send mail
    # send_mail(
    #     subject="Welcome to Our Instagram App 🎉",
    #     message=(
    #         f"Hi {instance.username},\n\n"
    #         f"Your account has been created successfully.\n\n"
    #         f"If you did NOT create this account, click below to delete it:\n"
    #         f"{delete_url}\n\n"
    #         f"This link is valid for 24 hours."
    #     ),
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     recipient_list=[instance.email],
    #     fail_silently=False,
    # )
