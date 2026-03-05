from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    university_id = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('supervisor', 'Supervisor'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
@property
def is_student(self):
    return self.role == 'student'

@property
def is_supervisor(self):