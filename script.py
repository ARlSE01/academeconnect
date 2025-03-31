import os
import django

# Step 1: Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academeconnect.settings')  # Update this with your actual settings module
django.setup()

from connect.models import Tags

predefined_tags = ['HTML', 'CSS', 'JS', 'Python', 'Django']
for tag_name in predefined_tags:
    Tags.objects.get_or_create(name=tag_name)

print("Predefined tags inserted!")