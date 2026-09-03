from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from authentication.models import CustomerProfile, TechnicianProfile
from fixnear.cache_key import customer_profile_key, technician_profile_key, technicianlist_key
from django.core.cache import cache

User=get_user_model()

@receiver(post_save, sender=User)
def ProfileCreateCustomerOrTechnician(sender, instance, created, **kwargs):
    if created:
        if instance.role=='CUSTOMER':
            CustomerProfile.objects.create(user=instance)
        TechnicianProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomerProfile)
def CustomerProfileCacheInvalidation(sender, instance, created, **kwargs):
    cache.delete(customer_profile_key(instance.user.id))

@receiver(post_save, sender=TechnicianProfile)
def TechnicianProfileCacheInvalidation(sender, instance, created, **kwargs):
    cache.delete(technician_profile_key(instance.user.id))
    for i in range(1, 100):
        cache.delete(technicianlist_key(i))