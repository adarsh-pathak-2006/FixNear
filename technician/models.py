from django.db import models
from authentication.models import TechnicianProfile
from customer.models import RepairRequest

class SentRequest(models.Model):
    technician=models.ForeignKey(TechnicianProfile, on_delete=models.CASCADE)
    request=models.ForeignKey(RepairRequest, on_delete=models.CASCADE)
    created_on=models.DateTimeField(auto_now_add=True)
    is_accepted=models.BooleanField(default=False)

    def __str__(self):
        return f"request:- {self.request.requirement} sent to {self.technician.user.username}"


class Repair(models.Model):
    accepted_request=models.OneToOneField(SentRequest, on_delete=models.CASCADE)
    status=models.CharField(max_length=10, choices=[('PENDING', 'Pending'), ('PROCESSING', 'Processing'), ('COMPLETED', 'Completed')], default='PENDING')
    updated_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.accepted_request.id} with status: {self.status}"