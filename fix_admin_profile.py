import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from portal.models import UserProfile

try:
    admin_user = User.objects.get(username='admin')
    # Check if profile exists
    if not hasattr(admin_user, 'userprofile'):
        print("Creating UserProfile for admin...")
        UserProfile.objects.create(user=admin_user, role='teacher', student_id='ADMIN', section='N/A')
        print("UserProfile created.")
    else:
        print("UserProfile already exists for admin.")
except User.DoesNotExist:
    print("Admin user does not exist.")
