# Generated by Django 4.1.7 on 2023-03-21 21:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aquaworld', '0003_alter_equipments_co2_alter_equipments_control_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='fish',
            unique_together={('aquarium', 'name')},
        ),
    ]
