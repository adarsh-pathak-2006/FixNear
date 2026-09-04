from django.db import models
from authentication.models import TechnicianProfile

class NotificationLog(models.Model):
    technician=models.ForeignKey(TechnicianProfile, on_delete=models.CASCADE)
    skill_required=models.CharField(max_length=100)
    requirement=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.technician.user.username

