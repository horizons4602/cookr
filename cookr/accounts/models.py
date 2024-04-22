from django.db import models
from django.conf import settings


class Profile(models.Model):
	SEX_CHOICES = (
		(0, 'Male'),
		(1, 'Female'),
	)
	GOAL_CHOICES = (
		(0, 'Maintain weight'),
		(1, 'Lose weight'),
		(2, 'Gain weight'),
	)
	ACTIVITY_LEVEL_CHOICES = (
		(0, 'Sedentary'),
		(1, 'Lightly active'),
		(2, 'Moderately active'),
		(3, 'Very active'),
		(4, 'Super active'),
	)

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
	age = models.IntegerField(default=0)
	sex = models.IntegerField(default=0, choices=SEX_CHOICES)
	height_in_inches = models.IntegerField(default=0)
	weight = models.IntegerField(default=0)
	activity_level = models.IntegerField(default=0, choices=ACTIVITY_LEVEL_CHOICES)
	goal = models.IntegerField(default=0, choices=GOAL_CHOICES)


class UserPreferences(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)

	sweetness = models.IntegerField(default=0)
	saltiness = models.IntegerField(default=0)
	sourness = models.IntegerField(default=0)
	bitterness = models.IntegerField(default=0)
	savoriness = models.IntegerField(default=0)
	fattiness = models.IntegerField(default=0)
	spiciness = models.IntegerField(default=0)


class UserAllergies(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)

	alcohol_cocktail = models.BooleanField(default=False)
	alcohol_free = models.BooleanField(default=False)
	celery_free = models.BooleanField(default=False)
	crustacean_free = models.BooleanField(default=False)
	dairy_free = models.BooleanField(default=False)
	egg_free = models.BooleanField(default=False)
	fish_free = models.BooleanField(default=False)
	fodmap_free = models.BooleanField(default=False)
	gluten_free = models.BooleanField(default=False)
	immuno_supportive = models.BooleanField(default=False)
	keto_friendly = models.BooleanField(default=False)
	kidney_friendly = models.BooleanField(default=False)
	kosher = models.BooleanField(default=False)
	low_fat_abs = models.BooleanField(default=False)
	low_potassium = models.BooleanField(default=False)
	low_sugar = models.BooleanField(default=False)
	lupine_free = models.BooleanField(default=False)
	Mediterranean = models.BooleanField(default=False)
	mollusk_free = models.BooleanField(default=False)
	mustard_free = models.BooleanField(default=False)
	no_oil_added = models.BooleanField(default=False)
	paleo = models.BooleanField(default=False)
	peanut_free = models.BooleanField(default=False)
	pescatarian = models.BooleanField(default=False)
	pork_free = models.BooleanField(default=False)
	red_meat_free = models.BooleanField(default=False)
	sesame_free = models.BooleanField(default=False)
	shellfish_free = models.BooleanField(default=False)
	soy_free = models.BooleanField(default=False)
	sugar_conscious = models.BooleanField(default=False)
	sulfite_free = models.BooleanField(default=False)
	tree_nut_free = models.BooleanField(default=False)
	vegan = models.BooleanField(default=False)
	vegetarian = models.BooleanField(default=False)
	wheat_free = models.BooleanField(default=False)


class UserAPIkeys(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)

	edamam_api_key = models.CharField(max_length=255)
	edamam_app_id = models.CharField(max_length=255)
	spoon_api_key = models.CharField(max_length=255)
