from django.db import models
from django.contrib.auth.models import User


def default_user():
    # Returns the first user, make sure a user exists or set it to a specific user ID
    return User.objects.first().id if User.objects.exists() else None


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', default=default_user)
    recipe_data = models.JSONField(default=dict)
    items_count = models.IntegerField(default=0)
    last_seen_index = models.IntegerField(default=-1)  # starts from -1 meaning no items seen

    def add_recipes(self, recipes):
        """ Append new recipes to the existing recipe data and update count. """
        for key, value in recipes.items():
            if key in self.recipe_data:
                # Ensure the existing data for the key is a list
                if not isinstance(self.recipe_data[key], list):
                    self.recipe_data[key] = [self.recipe_data[key]]
                self.recipe_data[key].extend(value if isinstance(value, list) else [value])
            else:
                self.recipe_data[key] = value if isinstance(value, list) else [value]
        self.items_count = len(self.recipe_data.get('Name', []))  # Safely get 'Name' or default to empty list
        self.save()

    def get_next_recipe(self):
        """ Return the next unseen recipe if available, skipping non-list data entries. """
        if self.last_seen_index + 1 < self.items_count:
            self.last_seen_index += 1
            self.save()
            # Exclude 'Items' and 'Seen' from the keys to be processed
            recipe_keys = [key for key in self.recipe_data if key not in ['Items', 'Seen']]
            try:
                return {key: self.recipe_data[key][self.last_seen_index] for key in recipe_keys}
            except TypeError as e:
                # Log the error and the problematic data
                print(f"Error accessing data: {e}")
                print({key: type(self.recipe_data[key]) for key in recipe_keys})  # This will show data types
                raise
        return None

    def get_current_recipe(self):
        recipe_keys = [key for key in self.recipe_data if key not in ['Items', 'Seen']]
        try:
            return {key: self.recipe_data[key][self.last_seen_index] for key in recipe_keys}
        except TypeError as e:
            # Log the error and the problematic data
            print(f"Error accessing data: {e}")
            print({key: type(self.recipe_data[key]) for key in recipe_keys})  # This will show data types
            raise


