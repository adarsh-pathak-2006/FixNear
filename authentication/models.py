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
    skill=models.CharField(max_length=100, choices=[('MOBILE_REPAIR', 'Mobile_Repair'), ('LAPTOP_REPAIR', 'Laptop_Repair'), ('PLUMBER', 'Plumber'), ('ELECTRICIAN', 'Electrician')], null=True)
    is_avaliable=models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
