from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import CustomerProfile, TechnicianProfile

User=get_user_model()

@receiver(post_save, sender=User)
def ProfileCreateCustomerOrTechnician(sender, instance, created, **kwargs):
    if created:
        if instance.role=='CUSTOMER':
            CustomerProfile.objects.create(user=instance)
        TechnicianProfile.objects.create(user=instance)