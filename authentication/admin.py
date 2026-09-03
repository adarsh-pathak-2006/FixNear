from django.contrib import admin
from .models import TechnicianProfile, CustomerProfile, TechnicalSkill

admin.site.register(TechnicianProfile)
admin.site.register(CustomerProfile)
admin.site.register(TechnicalSkill)
