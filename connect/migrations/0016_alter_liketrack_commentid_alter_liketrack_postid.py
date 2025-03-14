# Generated by Django 5.1.6 on 2025-03-06 16:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0015_liketrack'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liketrack',
            name='commentid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='liketrackcommentid', to='connect.post'),
        ),
        migrations.AlterField(
            model_name='liketrack',
            name='postid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='liketrackpostid', to='connect.post'),
        ),
    ]
