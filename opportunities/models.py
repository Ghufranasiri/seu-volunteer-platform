from django.db import models


class Opportunity(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    hours = models.PositiveIntegerField(help_text="Volunteer hours")
    location = models.CharField(max_length=255)
    date = models.DateField()
    organization = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "Opportunity"
        verbose_name_plural = "Opportunities"

    def __str__(self):
        return self.name


