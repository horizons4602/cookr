from django.db import models
from django.conf import settings


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField(max_length=500)
    site_url = models.URLField(max_length=500)
    calories = models.FloatField()
    time_to_cook = models.IntegerField(help_text="Time in minutes")
    fat = models.FloatField(help_text="Fat in grams")
    carbs = models.FloatField(help_text="Carbohydrates in grams")
    protein = models.FloatField(help_text="Protein in grams")
    ingredients = models.JSONField()

    class Meta:
        abstract = True


class SavedOne(Recipe):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='italian_recipe')


class SavedTwo(Recipe):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mexican_recipe')


class SavedThree(Recipe):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='indian_recipe')


class SavedFour(Recipe):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='french_recipe')


class SavedFive(Recipe):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chinese_recipe')


class SavedSix(Recipe):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='american_recipe')
