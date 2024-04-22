# Generated by Django 5.0.4 on 2024-04-22 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='macros',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='url',
        ),
        migrations.AddField(
            model_name='recipe',
            name='calories',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='recipe',
            name='carbs',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='recipe',
            name='fat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='recipe',
            name='items',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='recipe',
            name='protein',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='recipe',
            name='seen',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='recipe',
            name='site_url',
            field=models.URLField(default=None),
        ),
        migrations.AddField(
            model_name='recipe',
            name='time',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
