from faker import Faker
from random import random, randint
from faker.providers import DynamicProvider


# Creates random recipes
recipe_name_provider = DynamicProvider(
    provider_name="recipe_name",
    elements=["Creamy Garlic Alfredo Pasta",
        "Spicy Chicken Tikka Masala",
        "Lemon Herb Roasted Salmon",
        "Classic Beef Lasagna",
        "Honey Glazed Carrots",
        "Baked Macaroni and Cheese",
        "Mushroom Risotto",
        "Thai Green Curry with Jasmine Rice",
        "BBQ Pulled Pork Sandwiches",
        "Caprese Salad with Balsamic Drizzle",
        "Butternut Squash Soup",
        "Shrimp Scampi Linguine",
        "Margherita Pizza",
        "Korean Beef Bulgogi",
        "Chicken and Waffles",
        "Mediterranean Quinoa Bowl",
        "Crispy Tofu Stir-Fry",
        "Spinach and Feta Stuffed Peppers",
        "Teriyaki Glazed Chicken Wings",
        "Garlic Butter Steak Bites",
        "Eggplant Parmesan",
        "Sweet Potato Black Bean Tacos",
        "Lobster Bisque",
        "Breakfast Burrito Supreme",
        "Blueberry Lemon Muffins",
        "Homemade Cinnamon Rolls",
        "Grilled Veggie Panini",
        "Creamy Tomato Basil Soup",
        "Chocolate Lava Cake",
        "Mango Coconut Pudding"
    ],
)
measurement_provider = DynamicProvider(
    provider_name="measurement",
    elements=["cups",
        "oz",
        "",
        "lbs."
    ],
)
class FakeRecipe:
    def __init__(self, id):
        fake = Faker()
        fake.add_provider(recipe_name_provider)
        fake.add_provider(measurement_provider)

        self.name = fake.recipe_name()
        self.author = fake.name()
        self.id = id
        self.description = fake.paragraph()
        self.serving = randint(2,6)
        self.reviews = randint(1,200)
        meals = ['Breakfast', 'Lunch', 'Dinner', 'Snacks', 'Dessert']
        self.meal = meals[randint(0,4)]
        
        self.prep_time = randint(10, 75)
        self.cook_time = randint(30, 90)
        self.total_time = self.prep_time + self.cook_time
        if self.prep_time >= 60:
            self.prep_unit = "hr"
            self.prep_time = round(self.prep_time / 60, 2)
        else:
            self.prep_unit = "min"
        
        if self.cook_time >= 60:
            self.cook_unit = "hr"
            self.cook_time = round(self.cook_time / 60, 2)
        else:
            self.cook_unit = "min"

        temp = self.total_time
        self.total_time = [int(round(temp / 60, 0)), round(temp % 60, 2)]


        # Grabs a square image, different resolutions are different images
        temp_int = randint(100,1000)
        self.image = f"https://placecats.com/{temp_int}/{temp_int}"

        self.ingredients = []
        for i in range(randint(8,20)):
            temp_ing = []
            temp_ing.append(randint(0,10))
            temp_ing.append(fake.measurement())
            temp_ing.append(fake.word())
            self.ingredients.append(temp_ing)

        self.instructions = []
        for i in range(randint(5,20)):
            self.instructions.append(fake.sentence())

        # Adds a star based on what the rating is
        self.rating = random() * 4.1 + 1 # Grabs float from 1 to 5.1
        self.stars_html = ""
        j = self.rating
        for i in range(5):
            if j > 1:
                self.stars_html += "<span class='fa fa-star'></span> "
            elif j > 0:
                self.stars_html += "<span class='fa fa-star-half-full'></span> "
            else:
                self.stars_html += "<span class='fa fa-star-o'></span> "
            j -= 1
        self.rating_disp = round(self.rating,2)
        if self.rating_disp > 5:
            self.rating_disp = 5.0
recipes = [FakeRecipe(i) for i in range(30)]
