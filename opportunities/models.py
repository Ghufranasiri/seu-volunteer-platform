from django.db import models


class Opportunity(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    name = models.CharField(max_length=200)

    description = models.TextField()

    location = models.CharField(max_length=200)

    date = models.DateField()

    capacity = models.IntegerField(default=0)

    hours = models.IntegerField(default=1)

    organization = models.CharField(
        max_length=200,
        default="SEU Volunteer Agency"
    )

    category = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return self.name