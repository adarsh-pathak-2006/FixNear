from django.db import models
from django.contrib.auth.models import AbstractUser
from fixnear.constants import SKILL_CHOICES


class User(AbstractUser):
    ROLE_CHOICES = [
        ('TECHNICIAN', 'Technician'),
        ('CUSTOMER', 'Customer'),
        ('ADMIN', 'Admin'),
    ]

    mobile_no = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CUSTOMER')


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class TechnicianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    experience = models.PositiveIntegerField(null=True, blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    total_job = models.PositiveIntegerField(default=0)
    skill = models.CharField(max_length=100, choices=SKILL_CHOICES, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
