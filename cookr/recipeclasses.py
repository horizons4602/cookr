class Recipe:
    def __init__(self, id, selfHref, image, url, title, ingredients, calories, totalWeight, totalTime, protein, carbs, fat, sugar, sodium):
        self.id = id # Database ID, not from API
        self.selfHref = selfHref
        self.image = image
        self.url = url
        self.title = title
        self.ingredients = ingredients
        self.calories = calories
        self.totalWeight = totalWeight
        self.totalTime = totalTime
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.sugar = sugar
        self.sodium = sodium
    
    def __str__(self):
        return f"ID: {self.id}\n selfHref: {self.selfHref}\n Image {self.image}\nURL: {self.url}\nTitle: {self.title}\nIngredients: {self.ingredients}\nCalories: {self.calories}\nTotal Weight: {self.totalWeight}\nTotal Time: {self.totalTime}\nProtein: {self.protein}\nCarbs: {self.carbs}\nFat: {self.fat}\nSugar: {self.sugar}\nSodium: {self.sodium}"

class RecipeDesc:
        def __init__(self, sweetness, saltiness, sourness, bitterness, savoriness, fattiness, spiciness):
            self.sweetness = sweetness
            self.saltiness = saltiness
            self.sourness = sourness
            self.bitterness = bitterness
            self.savoriness = savoriness
            self.fattiness = fattiness
            self.spiciness = spiciness
        def __str__(self):
            return f"Sweetness: {self.sweetness}\nSaltiness: {self.saltiness}\nSourness: {self.sourness}\nBitterness: {self.bitterness}\nSavouriness: {self.savoriness}\nFattiness: {self.fattiness}\nSpiciness: {self.spiciness}"
        
class RecipeRecommendation:
    def __init__(self, sweetness, saltiness, sourness, bitterness, savoriness, fattiness, spiciness, calories, protein, carbs, fat, sugar, sodium):
        self.sweetness = sweetness
        self.saltiness = saltiness
        self.sourness = sourness
        self.bitterness = bitterness
        self.savoriness = savoriness
        self.fattiness = fattiness
        self.spiciness = spiciness
        # Percentage of daily values
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.sugar = sugar
        self.sodium = sodium
    def __str__(self):
         return f"Sweetness: {self.sweetness}\nSaltiness: {self.saltiness}\nSourness: {self.sourness}\nBitterness: {self.bitterness}\nSavouriness: {self.savoriness}\nFattiness: {self.fattiness}\nSpiciness: {self.spiciness}\nCalories: {self.calories}\nProtein: {self.protein}\nCarbs: {self.carbs}\nFat: {self.fat}\nSugar: {self.sugar}\nSodium: {self.sodium}"