from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES=[('TECHNICIAN', 'Technician'), ('CUSTOMER', 'Customer'), ('ADMIN', 'Admin')]

    mobile_no=models.CharField(max_length=15, unique=True)
    role=models.CharField(max_length=10, choices=ROLE_CHOICES, default='CUSTOMER')

class CustomerProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    latitute=models.CharField(max_length=20, null=True)
    longitude=models.CharField(max_length=20, null=True)
    is_verified=models.BooleanField(default=False)
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class TechnicianProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    bio=models.TextField(null=True)
    experience=models.PositiveIntegerField(null=True)
    average_rating=models.IntegerField(null=True)
    total_job=models.PositiveIntegerField(default=0)
    is_avaliable=models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class TechnicalSkill(models.Model):
    user=models.ForeignKey(TechnicianProfile, on_delete=models.CASCADE)
    skill_name=models.CharField(max_length=50)
    experience_level=models.PositiveIntegerField(max_length=5)
    description=models.TextField(null=True)

    def __str__(self):
        return self.skill_name