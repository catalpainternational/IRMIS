from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Road


@receiver(pre_save, sender=Road)
def pre_save_road(sender, instance, **kwargs):
    if not instance._state.adding:
        old_instance = Road.objects.get(id=instance.id)
        if old_instance == instance:
            raise ValueError("Nothing to save")
