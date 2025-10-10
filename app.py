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
recipe_title_provider = DynamicProvider(
    provider_name="recipe_title",
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
    def __init__(self):
        fake = Faker()
        fake.add_provider(recipe_title_provider)
        fake.add_provider(measurement_provider)

        self.title = fake.recipe_title()
        self.stars = random() * 4 + 1 #Makes number 1-to five
        self.author = fake.name()
        self.ingredients = []
        temp_int = randint(100,1000)
        self.image = f"https://placecats.com/{temp_int}/{temp_int}"
        for i in range(randint(4,10)):
            temp_ing = []
            temp_ing.append(randint(0,10))
            temp_ing.append(fake.measurement())
            temp_ing.append(fake.word())
            self.ingredients.append(temp_ing)
        self.instructions = []
        for i in range(randint(5,20)):
            self.instructions.append(fake.sentence())
        self.stars_html = ""
        j = self.stars
        print(j)
        for i in range(5):
            j -= 1
            print(j)
            if j > 1:
                self.stars_html += "<span class='fa fa-star'></span> "
            elif j > 0:
                self.stars_html += "<span class='fa fa-star-half-full'></span> "
            else:
                self.stars_html += "<span class='fa fa-star-o'></span> "

recipes = [Recipe() for i in range(30)]

@app.route('/')
def index():
    print("test")
    return render_template('index.html')

@app.route('/cookbook')
def cookbook():
    r = [ 
        {"src": "peppers2.jpg",
        "href": "/peppers",
        "name": "Cream Cheese Stuffed Peppers",
        "stars": "<span class='fa fa-star'></span> "
                "<span class='fa fa-star'></span> "
                "<span class='fa fa-star'></span> "
                "<span class='fa fa-star'></span> "
                "<span class='fa fa-star-half-full'></span> "}]
    for rec in recipes:
        r += [{
            "src": rec.image,
            "href": "",
            "name": rec.title,
            "stars": rec.stars_html}]

    return render_template('cookbook.html', recipes=r)

@app.route('/peppers')
def peppers():
    return render_template('peppers.html')

@app.route('/new-recipe', methods=['GET', 'POST'])
def new_recipe():
    # if request.method == 'POST':
    #     name = request.form.get('name')
    #     serving = request.form.get('serving')
    #     prep_time  = request.form.get('prep-time')
    #     prep_units  = request.form.get('prep-units')
    #     cook_time = request.form.get('cook-time')
    #     cook_units = request.form.get('cook-units')
    #     amount = request.form.get('amount')
    #     measurement = request.form.get('measurement')
    #     food = request.form.get('food')
    #     instruction = request.form.get('instruction')
    #     return f"{name}, {serving}\n, {prep_time}, {prep_units}, {cook_time}, {cook_units}"

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

    return cookbook()
    
    

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
