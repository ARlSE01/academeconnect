from models import Tags

predefined_tags = ['HTML', 'CSS', 'JS', 'Python', 'Django']
for tag_name in predefined_tags:
    Tags.objects.get_or_create(name=tag_name)

print("Predefined tags inserted!")