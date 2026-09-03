from django.db import models
from authentication.models import TechnicianProfile
from customer.models import RepairRequest

class AcceptedRequest(models.Model):
    technician=models.ForeignKey(TechnicianProfile, on_delete=models.CASCADE)
    request=models.OneToOneField(RepairRequest, on_delete=models.CASCADE)
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"request:- {self.request.requirement} accepted by {self.technician.user.username}"
