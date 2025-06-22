from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Suggestion, Notification, CustomUser, Role
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Suggestion)
def notify_admin_on_suggestion_create(sender, instance, created, **kwargs):
    if created:
        admins = CustomUser.objects.filter(is_superuser=True)
        for admin in admins:
            Notification.objects.create(
                user=admin,
                message=f"Новое предложение: «{instance.title}» от {instance.user.get_full_name()}",
            )



