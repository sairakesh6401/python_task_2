from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
    )

class PatientProfile(models.Model):
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    

class DoctorProfile(models.Model):
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    
