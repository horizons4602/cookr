# Generated by Django 5.0.4 on 2024-04-19 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_edemam_api_key_userapikeys_edamam_api_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userapikeys',
            name='edamam_api_key',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='userapikeys',
            name='edamam_app_id',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='userapikeys',
            name='spoon_api_key',
            field=models.CharField(default='', max_length=255),
        ),
    ]