# Generated by Django 5.0.4 on 2024-04-22 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('image_url', models.URLField()),
                ('ingredients', models.TextField()),
                ('macros', models.TextField()),
            ],
        ),
    ]