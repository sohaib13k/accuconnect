# Generated by Django 5.0.6 on 2024-06-08 12:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_request_count', models.IntegerField(default=0)),
                ('sent_request_tmstmp', models.DateTimeField(auto_now_add=True)),
                ('friends', models.ManyToManyField(to='userprofile.userprofile')),
                ('pending_requests', models.ManyToManyField(to='userprofile.userprofile')),
                ('sent_requests', models.ManyToManyField(to='userprofile.userprofile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
