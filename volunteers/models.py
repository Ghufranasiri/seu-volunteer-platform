from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from users.models import CustomUser


class Organization(models.Model):
    """منظمة أو جهة تطوع"""
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    website = models.URLField(blank=True, null=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='organizations/', blank=True, null=True)
    
    # الموقع
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    # الحالة
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # البيانات الإدارية
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # الربط مع المستخدم (مدير المنظمة)
    manager = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, related_name='organization')
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Organizations'
    
    def __str__(self):
        return self.name


class Category(models.Model):
    """فئات الفرص التطوعية"""
    CATEGORY_CHOICES = (
        ('education', 'التعليم'),
        ('health', 'الصحة والرعاية'),
        ('environment', 'البيئة'),
        ('community', 'خدمة المجتمع'),
        ('arts', 'الفنون والثقافة'),
        ('sports', 'الرياضة'),
        ('technology', 'التكنولوجيا'),
        ('other', 'آخرى'),
    )
    
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, unique=True)
    icon = models.CharField(max_length=50, blank=True)  # Font Awesome icon
    color = models.CharField(max_length=7, default='#667eea')  # Hex color
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.get_name_display()


class Opportunity(models.Model):
    """فرصة تطوعية"""
    DIFFICULTY_CHOICES = (
        ('beginner', 'سهل'),
        ('intermediate', 'متوسط'),
        ('advanced', 'متقدم'),
    )
    
    STATUS_CHOICES = (
        ('draft', 'مسودة'),
        ('published', 'منشورة'),
        ('closed', 'مغلقة'),
        ('cancelled', 'ملغاة'),
    )
    
    # البيانات الأساسية
    title = models.CharField(max_length=200)
    description = models.TextField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='opportunities')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    # التفاصيل
    required_hours = models.IntegerField(validators=[MinValueValidator(1)])
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    max_volunteers = models.IntegerField(validators=[MinValueValidator(1)])
    
    # الموقع والوقت
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    # المتطلبات والمهارات
    requirements = models.TextField(blank=True, help_text='المتطلبات المطلوبة')
    skills = models.CharField(max_length=255, blank=True, help_text='المهارات المطلوبة (مفصولة بفواصل)')
    
    # الصورة
    image = models.ImageField(upload_to='opportunities/', blank=True, null=True)
    
    # الحالة
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    
    # البيانات الإدارية
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='created_opportunities')
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'start_date']),
            models.Index(fields=['organization', 'status']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_available_spots(self):
        """عدد الأماكن المتبقية"""
        registered = self.registrations.filter(status='approved').count()
        return self.max_volunteers - registered
    
    @property
    def is_active(self):
        """هل الفرصة نشطة الآن"""
        return self.status == 'published' and self.start_date <= timezone.now() <= self.end_date
    
    @property
    def registered_count(self):
        """عدد المتطوعين المسجلين"""
        return self.registrations.filter(status='approved').count()


class VolunteerRegistration(models.Model):
    """تسجيل متطوع في فرصة"""
    STATUS_CHOICES = (
        ('pending', 'قيد الانتظار'),
        ('approved', 'موافق عليه'),
        ('rejected', 'مرفوض'),
        ('cancelled', 'ملغى'),
    )
    
    volunteer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='registrations')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='registrations')
    
    # الحالة
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # السجل
    registered_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    
    # ملاحظات
    notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True, help_text='سبب الرفض إن وجد')
    
    class Meta:
        unique_together = ('volunteer', 'opportunity')
        ordering = ['-registered_at']
    
    def __str__(self):
        return f"{self.volunteer.username} - {self.opportunity.title}"


class VolunteerHours(models.Model):
    """تسجيل ساعات التطوع"""
    STATUS_CHOICES = (
        ('pending', 'قيد المراجعة'),
        ('approved', 'معتمد'),
        ('rejected', 'مرفوض'),
    )
    
    volunteer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='hours')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='volunteer_hours')
    
    # الساعات
    hours = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.5)])
    date_completed = models.DateField()
    
    # الحالة
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # الملاحظات
    description = models.TextField(blank=True)
    
    # للمراجع
    reviewed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, 
                                     related_name='reviewed_hours')
    reviewed_at = models.DateTimeField(blank=True, null=True)
    review_notes = models.TextField(blank=True)
    
    # البيانات الإدارية
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_completed']
        indexes = [
            models.Index(fields=['volunteer', 'status']),
            models.Index(fields=['date_completed']),
        ]
    
    def __str__(self):
        return f"{self.volunteer.username} - {self.hours}h on {self.date_completed}"


class Certificate(models.Model):
    """شهادة تقدير"""
    LEVEL_CHOICES = (
        ('bronze', 'برونزي'),
        ('silver', 'فضي'),
        ('gold', 'ذهبي'),
        ('platinum', 'بلاتيني'),
    )
    
    volunteer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='certificates')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.SET_NULL, null=True, blank=True, 
                                     related_name='certificates')
    
    # البيانات
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='bronze')
    
    # الساعات
    total_hours = models.DecimalField(max_digits=5, decimal_places=2)
    
    # التواريخ
    issued_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(blank=True, null=True)
    
    # التحقق
    is_verified = models.BooleanField(default=True)
    verification_code = models.CharField(max_length=50, unique=True)
    
    # الملف
    pdf_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    
    class Meta:
        ordering = ['-issued_date']
    
    def __str__(self):
        return f"{self.title} - {self.volunteer.first_name}"


class Review(models.Model):
    """تقييم ومراجعة الفرصة"""
    RATING_CHOICES = (
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    )
    
    volunteer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='reviews')
    
    # التقييم
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    comment = models.TextField()
    
    # البيانات الإدارية
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # المراجع
    is_verified = models.BooleanField(default=False)  # تم التحقق من أن هذا المستخدم اكمل الفرصة فعلاً
    
    class Meta:
        unique_together = ('volunteer', 'opportunity')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.volunteer.username} - {self.opportunity.title}"


class Impact(models.Model):
    """تتبع تأثير التطوع"""
    volunteer = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='impact')
    
    # الإحصائيات
    total_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_opportunities = models.IntegerField(default=0)
    total_certificates = models.IntegerField(default=0)
    
    # نقاط التأثير
    impact_points = models.IntegerField(default=0)  # نقاط تحسب بناءً على الساعات والشهادات
    
    # البيانات الإدارية
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Impacts'
    
    def __str__(self):
        return f"Impact - {self.volunteer.username}"
    
    def calculate_impact_points(self):
        """حساب نقاط التأثير"""
        # نقطة واحدة لكل ساعة + 10 نقاط لكل شهادة
        return int(self.total_hours) + (self.total_certificates * 10)


class Announcement(models.Model):
    """إعلانات منتدى"""
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='announcements', 
                                      blank=True, null=True)
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # الأولويات
    is_featured = models.BooleanField(default=False)
    
    # البيانات الإدارية
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
