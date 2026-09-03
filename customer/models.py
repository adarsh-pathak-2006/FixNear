from django.db import models
from authentication.models import CustomerProfile

class RepairRequest(models.Model):
    user=models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    skills_required=models.CharField(max_length=100, choices=[('MOBILE_REPAIR', 'Mobile_Repair'), ('LAPTOP_REPAIR', 'Laptop_Repair'), ('PLUMBER', 'Plumber'), ('ELECTRICIAN', 'Electrician')])
    requirement=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.requirement[:50]

