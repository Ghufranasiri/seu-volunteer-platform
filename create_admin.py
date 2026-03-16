#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create primary superuser if not exists
# NOTE: the Django admin site uses the `username` field, not the email.
# by default the script creates a user whose username is literally
# "admin".  If you attempt to log in with the email address you'll see
# the "correct username and password for a staff account" error, because
# the username really is "admin".
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@seu.edu.sa',
        password='admin123456'
    )
    print("✅ Superuser 'admin' created successfully!")
    print("Username: admin")
    print("Password: admin123456")
    print("Email: admin@seu.edu.sa")
else:
    print("⚠️ Admin user already exists!")

# OPTIONAL: if you prefer to be able to log in using the email address as
# the username, create a second superuser with the same password.
if not User.objects.filter(username='admin@seu.edu.sa').exists():
    User.objects.create_superuser(
        username='admin@seu.edu.sa',
        email='admin@seu.edu.sa',
        password='admin123456'
    )
    print("✅ Superuser 'admin@seu.edu.sa' created as an email-username alias.")


# Create some test Categories
from volunteers.models import Category

categories_data = [
    ('education', 'التعليم'),
    ('health', 'الصحة والرعاية'),
    ('environment', 'البيئة'),
    ('community', 'خدمة المجتمع'),
    ('arts', 'الفنون والثقافة'),
]

for code, name in categories_data:
    Category.objects.get_or_create(
        name=code,
        defaults={'color': '#667eea'}
    )

print("✅ Categories created successfully!")
