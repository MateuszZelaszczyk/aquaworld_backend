# Generated by Django 4.1.7 on 2023-03-29 18:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aquaworld', '0012_alter_comments_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='friend_of', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_requests', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('from_user', 'to_user')},
            },
        ),
        migrations.AddField(
            model_name='users',
            name='friend_requests',
            field=models.ManyToManyField(blank=True, related_name='requested_friend_of', through='aquaworld.FriendRequest', to=settings.AUTH_USER_MODEL),
        ),
    ]
