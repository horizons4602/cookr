# Generated by Django 5.0.4 on 2024-04-22 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_profile_sex'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='calories',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='carbs',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='fat',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='protein',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='sodium',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='sugar',
        ),
    ]
