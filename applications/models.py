from django.db import models
from django.conf import settings

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'), # الإضافة الجديدة
    ]

    # الحقول السابقة (تأكدي من مطابقتها لمشروعك)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # اضفت السطر تحت بتعليق عشان لو اسم المجلد عندك مختلف
    # opportunity = models.ForeignKey('opportunities.Opportunity', on_delete=models.CASCADE)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # حقل الساعات الجديد
    volunteer_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    applied_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Application {self.id} - {self.status}"
