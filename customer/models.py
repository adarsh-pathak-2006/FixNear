from django.db import models
from authentication.models import CustomerProfile
from fixnear.constants import SKILL_CHOICES


class RepairRequest(models.Model):
    user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    skills_required = models.CharField(max_length=100, choices=SKILL_CHOICES)
    requirement = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.requirement[:50]
