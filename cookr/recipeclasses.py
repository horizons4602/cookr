class Recipe:
    def __init__(self, id, selfHref, image, url, title, ingredients, calories, totalWeight, totalTime):
        self.id = id # Database ID, not from API
        self.selfHref = selfHref
        self.image = image
        self.url = url
        self.title = title
        self.ingredients = ingredients
        self.calories = calories
        self.totalWeight = totalWeight
        self.totalTime = totalTime
    
    def __str__(self):
        return f"ID: {self.id}\n selfHref: {self.selfHref}\n Image {self.image}\nURL: {self.url}\nTitle: {self.title}\nIngredients: {self.ingredients}\nCalories: {self.calories}\nTotal Weight: {self.totalWeight}\nTotal Time: {self.totalTime}"

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