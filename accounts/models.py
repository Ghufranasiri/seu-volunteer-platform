from django.db import models
from django.contrib.auth.models import User

class Opportunity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()

    def __str__(self):
        return self.title


class Registration(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Pending')  # Approved / Rejected
    hours = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.username} - {self.opportunity.title}"eate your models here.
