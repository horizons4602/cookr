from django.db import models
from django.conf import settings


class Recipe(models.Model):
    name = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    site_url = models.URLField(max_length=500, blank=True)
    calories = models.FloatField(null=True)
    time_to_cook = models.IntegerField(help_text="Time in minutes", null=True)
    fat = models.FloatField(help_text="Fat in grams", null=True)
    carbs = models.FloatField(help_text="Carbohydrates in grams", null=True)
    protein = models.FloatField(help_text="Protein in grams", null=True)
    ingredients = models.JSONField(blank=True, null=True)

    class Meta:
        abstract = True


class SavedOne(Recipe):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_one')


class SavedTwo(Recipe):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_two')


class SavedThree(Recipe):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_three')


class SavedFour(Recipe):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_four')


class SavedFive(Recipe):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_five')


class SavedSix(Recipe):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_six')
