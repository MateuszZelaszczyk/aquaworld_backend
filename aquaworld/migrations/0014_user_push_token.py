# Generated by Django 4.1.7 on 2023-04-03 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aquaworld', '0013_users_friends_friendrequest_users_friend_requests'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_push_token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=1000)),
            ],
        ),
    ]