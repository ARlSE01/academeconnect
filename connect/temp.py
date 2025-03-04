from django.contrib.auth.models import User

# Create superuser if it doesn't exist
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "adminpassword")
    print("Superuser created successfully!")
else:
    print("Superuser already exists.")
