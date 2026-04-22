from django.db import models
from django.contrib.auth.models import AbstractUser


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
        return self.role == 'supervisor'

    def __str__(self):
        return self.username


class Certificate(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    opportunity = models.ForeignKey('opportunities.Opportunity', on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.opportunity.name}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'opportunity'],
                name='unique_user_opportunity_certificate'
            )
        ]