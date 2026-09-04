from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.db import transaction
from authentication.models import CustomerProfile, TechnicianProfile
from fixnear.cache_key import (
    customer_profile_key,
    technician_profile_key,
    technicianlist_key,
    repairrequest_list_key,
)
from django.core.cache import cache
from customer.models import RepairRequest
from technician.models import SentRequest

User = get_user_model()


@receiver(post_save, sender=User)
def ProfileCreateCustomerOrTechnician(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'CUSTOMER':
            CustomerProfile.objects.create(user=instance)
        elif instance.role == 'TECHNICIAN':
            TechnicianProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomerProfile)
def CustomerProfileCacheInvalidation(sender, instance, created, **kwargs):
    cache.delete(customer_profile_key(instance.user.id))


@receiver(post_save, sender=TechnicianProfile)
def TechnicianProfileCacheInvalidation(sender, instance, created, **kwargs):
    cache.delete(technician_profile_key(instance.user.id))
    keys = [technicianlist_key(i) for i in range(1, 101)]
    cache.delete_many(keys)


@receiver(post_save, sender=RepairRequest)
def SendRequestToTheAppropriateTechnicians(sender, instance, created, **kwargs):
    if created:
        from fixnear.tasks import dispatch_repair_request
        transaction.on_commit(lambda: dispatch_repair_request.delay(instance.pk))


@receiver(post_save, sender=SentRequest)
def CacheInvalidationWhenNewRequestCreatedOrApproved(sender, instance, created, **kwargs):
    keys = [
        repairrequest_list_key(page_no=i, userid=instance.technician.user.id)
        for i in range(1, 101)
    ]
    cache.delete_many(keys)
