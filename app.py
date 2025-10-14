# To activate virtual environment:
# Set-ExecutionPolicy RemoteSigned –Scope Process
# env\Scripts\Activate
# flask run --debug

from flask import Flask, render_template, request, redirect
# Libraries for Faker
from faker import Faker
from faker.providers import DynamicProvider
from random import random, randint

app = Flask(__name__)

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

class Recipe:
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

recipes = [Recipe(i) for i in range(50)]

@app.route('/')
def index():
    r = []
    for rec in recipes:
        r += [{
            "src": rec.image,
            "href": "",
            "name": rec.name,
            "stars": rec.stars_html,
            "id": rec.id
            }]
    return render_template('index.html', recipes=r)


@app.route('/cookbook')
def cookbook():
    r = [ 
        # {"src": "peppers2.jpg",
        # "href": "/peppers",
        # "name": "Cream Cheese Stuffed Peppers",
        # "stars": "<span class='fa fa-star'></span> "
        #         "<span class='fa fa-star'></span> "
        #         "<span class='fa fa-star'></span> "
        #         "<span class='fa fa-star'></span> "
        #         "<span class='fa fa-star-half-full'></span> "}
        ]
    for rec in recipes:
        r += [{
            "src": rec.image,
            "href": "",
            "name": rec.name,
            "stars": rec.stars_html,
            "id": rec.id
            }]

    return render_template('cookbook.html', recipes=r)


@app.route('/peppers')
def peppers():
    return render_template('peppers.html')

@app.route('/recipe/<id>')
def recipe_ex(id=0):
    print(id)
    recipe = recipes[int(id)]
    print(recipe)
    return render_template('recipe-example.html', r=recipe)


@app.route('/new-recipe')
def new_recipe():
    return render_template('enter-recipe.html')

@app.route('/submit-recipe', methods=['POST'])
def submit_recipe():
    print(request.form['name'])
    print(request.form['serving'])
    print(request.form['prep-time'])
    print(request.form['prep-units'])
    print(request.form['cook-time'])
    print(request.form['cook-units'])
    print(request.form['amount'])
    print(request.form['measurement'])
    print(request.form['food'])
    print(request.form['instruction'])
    return cookbook()   # Not sure how to properly redirect after form submission
    
    
@app.route('/log-in')
def log_in():
    return render_template('log-in.html')

@app.route('/submit-log-in', methods=['POST'])
def submit_log_in():
    print(request.form['email'])
    print(request.form['password'])
    # Add error checking for valid email
    return render_template('index.html')


@app.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')

@app.route('/submit-sign-up', methods=['POST'])
def submit_sign_up():
    print(request.form['email'])
    print(request.form['password'])
    # Add error checking for valid email
    return render_template('index.html')
