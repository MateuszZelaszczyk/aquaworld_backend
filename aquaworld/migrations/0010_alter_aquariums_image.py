# Generated by Django 4.1.7 on 2023-03-28 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aquaworld', '0009_remove_aquariums_is_editing_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aquariums',
            name='image',
            field=models.ImageField(default='profile/Avatar.png', upload_to='images/'),
        ),
    ]
