from django import forms


class RecipeReplaceForm(forms.Form):
    RECIPE_CHOICES = [
        ('saved_one', 'Saved One'),
        ('saved_two', 'Saved Two'),
        ('saved_three', 'Saved Three'),
        ('saved_four', 'Saved Four'),
        ('saved_five', 'Saved Five'),
        ('saved_six', 'Saved Six'),
    ]

    recipe_choice = forms.ChoiceField(
        choices=RECIPE_CHOICES,
        widget=forms.RadioSelect
    )
