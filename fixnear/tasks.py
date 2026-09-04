from celery import shared_task


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def dispatch_repair_request(self, repair_request_id):
    from customer.models import RepairRequest
    from authentication.models import TechnicianProfile
    from technician.models import SentRequest

    try:
        instance = RepairRequest.objects.get(pk=repair_request_id)
    except RepairRequest.DoesNotExist:
        return

    profiles = (
        TechnicianProfile.objects
        .select_related('user')
        .filter(skill=instance.skills_required, is_available=True)
    )

    for profile in profiles:
        SentRequest.objects.get_or_create(technician=profile, request=instance)

