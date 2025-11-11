# To activate virtual environment:
# env\Scripts\Activate
# flask run --debug

# To generate db:
# flask db init
# flask db upgrade

# To update db:
# flask db migrate
# flask db upgrade
# sqlite_web app.db -p 5050

from flask import Flask, flash, render_template, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sqlalchemy.orm as so
import sqlalchemy as sa
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from faker import Faker
from faker.providers import DynamicProvider
from random import random, randint

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
login = LoginManager(app)

basedir=os.path.abspath(os.path.dirname(__file__)) # Computer finds directory of project
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.db") # app.db defines database filename
db = SQLAlchemy(app) # db object represents the database
migrate = Migrate(app, db)
 


class User(UserMixin, db.Model):
    id:so.Mapped[int] = so.mapped_column(primary_key=True)
    username:so.Mapped[str] = so.mapped_column(default="Default username")
    email:so.Mapped[str] = so.mapped_column(default="Default email")
    password_hash:so.Mapped[str] = so.mapped_column(default="Default password")
    defaultVisibility:so.Mapped[int] = so.mapped_column(default=1)
    # Private = 0
    # Link only = 1
    # Public = 2
    def __init__(self):
        pass

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Recipe(db.Model):
    id:so.Mapped[int] = so.mapped_column(primary_key=True)
    name:so.Mapped[str] = so.mapped_column(index=True, default="Default name")
    meal:so.Mapped[str] = so.mapped_column(index=True, default="Default meal")
    servings:so.Mapped[int] = so.mapped_column(default=0)
    prepTime:so.Mapped[float] = so.mapped_column(default=0.0)
    prepUnit:so.Mapped[str] = so.mapped_column(default="Default unit")
    cookTime:so.Mapped[float] = so.mapped_column(default=0.0)
    cookUnit:so.Mapped[str] = so.mapped_column(default="Default unit")
    description:so.Mapped[str] = so.mapped_column(default="Default description")
    instructions:so.Mapped[str] = so.mapped_column(default="Default instructions")
    visibility:so.Mapped[int] = so.mapped_column(index=True, default=1)
    # Private = 0
    # Link only = 1
    # Public = 2
    image:so.Mapped[str] = so.mapped_column(default='Image string')
    author_id:so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    def __init__(self):
        pass


class Ingredient(db.Model):
    id:so.Mapped[int] = so.mapped_column(primary_key=True)
    name:so.Mapped[str] = so.mapped_column(index=True, default="Default name") 
    def __init__(self):
        pass

class IngredientEntry(db.Model):
    id:so.Mapped[int] = so.mapped_column(primary_key=True)
    amount:so.Mapped[float] = so.mapped_column(default=0.0)
    unit:so.Mapped[str] = so.mapped_column(default="Default unit")
    ingredient_id:so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    recipe_id:so.Mapped[int] = so.mapped_column(sa.ForeignKey(Recipe.id))
    def __init__(self):
        pass

class Substitute(db.Model):
    id:so.Mapped[int] = so.mapped_column(primary_key=True)
    amount:so.Mapped[float] = so.mapped_column(default=0.0)
    unit:so.Mapped[str] = so.mapped_column(default="Default unit")
    ingredient_id:so.Mapped[int] = so.mapped_column(sa.ForeignKey(Ingredient.id))
    ingredientEntry_id:so.Mapped[int] = so.mapped_column(sa.ForeignKey(IngredientEntry.id))
    recipe_id:so.Mapped[int] = so.mapped_column(sa.ForeignKey(Recipe.id))
    def __init__(self):
        pass

class CookbookEntry(db.Model):
    id:so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id:so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    recipe_id:so.Mapped[int] = so.mapped_column(sa.ForeignKey(Recipe.id))
    def __init__(self):
        pass

class Rating(db.Model):
    id:so.Mapped[int] = so.mapped_column(primary_key=True)
    value:so.Mapped[float] = so.mapped_column(default=0.0)
    recipe_id:so.Mapped[int] = so.mapped_column(sa.ForeignKey(Recipe.id))
    user_id:so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    def __init__(self):
        pass

class Note(db.Model):
    id:so.Mapped[int] = so.mapped_column(primary_key=True)
    text:so.Mapped[str] = so.mapped_column(default="")
    recipe_id:so.Mapped[int] = so.mapped_column(sa.ForeignKey(Recipe.id))
    user_id:so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    def __init__(self):
        pass

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



@app.route('/')
def index():
    query = sa.select(Recipe)
    d = db.session.scalars(query).all()
    breakfast = []
    lunch = []
    dinner = []
    snacks = []
    desserts = []
    # Need to add a querry for Rating to as to have a way to select which recipes should show up
    # Each meal should have 11 elements then a button to see more
    r = []
    for rec in recipes:
        r += [{
            "src": rec.image,
            "href": "",
            "name": rec.name,
            "stars": rec.stars_html,
            "id": rec.id
            }]
    return render_template('index.html', recipes=r, breakfast=breakfast, lunch=lunch, dinner=dinner, snacks=snacks, desserts=desserts)


@app.route('/cookbook')
def cookbook():
    query = sa.select(CookbookEntry)
    d = db.session.scalars(query).all()
    # return all Recipes that are linked to the user in the entry
    r = []
    # r = [ 
    #     {"src": "peppers2.jpg",
    #     "href": "/peppers",
    #     "name": "Cream Cheese Stuffed Peppers",
    #     "stars": "<span class='fa fa-star'></span> "
    #             "<span class='fa fa-star'></span> "
    #             "<span class='fa fa-star'></span> "
    #             "<span class='fa fa-star'></span> "
    #             "<span class='fa fa-star-half-full'></span> "}
    #     ]
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
    recipe = []
    recipe = recipes[int(id)]
    return render_template('recipe-example.html', r=recipe)


@app.route('/new-recipe')
def new_recipe():
    return render_template('enter-recipe.html')

@app.route('/submit-recipe', methods=['POST'])
def submit_recipe():
    # print(request.form['name'])
    # print(request.form['serving'])
    # print(request.form['prep-time'])
    # print(request.form['prep-units'])
    # print(request.form['cook-time'])
    # print(request.form['cook-units'])
    # print(request.form['amount'])
    # print(request.form['measurement'])
    # print(request.form['food'])
    # print(request.form['instruction'])
    r = Recipe()
    r.name = request.form['name']
    r.serving = request.form['serving']
    r.prep_time = request.form['prep-time']
    r.prep_unit = request.form['prep-units']
    r.cook_time = request.form['cook-time']
    r.cook_unit = request.form['cook-units']
    # request.form['amount'] 
    # request.form['measurement']
    # r.ingredient = request.form['food']
    r.instructions = request.form['instruction']
    r.author_id = 0
    db.session.add(r)
    db.session.commit()
    return redirect(url_for('cookbook'))   # Not sure how to properly redirect after form submission





# User authentication routes

# Is there a way to not erase all the data when redirecting back to the page
# flash() secret key???
# When do I even need to use  methods=['GET', 'POST'], Ive never used it so far

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

@app.route('/log-in')
def log_in():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('log-in.html')

@app.route('/submit-log-in', methods=['POST'])
def submit_log_in():
    user = db.session.scalar(sa.select(User).where(User.username == request.form['username']))
    if user is None or not user.check_password(request.form['password']):
        # flash('Invalid username or password')
        return redirect(url_for('log_in'))
    login_user(user, remember=request.form)
    # Dont know what the correct input for remember is
    return redirect(url_for('index'))


@app.route('/sign-up')
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('sign-up.html')


# Need add some type of uniqueness 
@app.route('/submit-sign-up', methods=['POST'])
def submit_sign_up():
    # Add error checking for valid email?
    if request.form['email1'] != request.form['email2']:
        # Flash not working
        flash('Emails do not match')
        return redirect(url_for('sign_up'))
    
    user = User()
    user.username = request.form['username']
    user.email = request.form['email1']
    hash = generate_password_hash(request.form['password'])
    user.password_hash = hash
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=request.form)

    return redirect(url_for('index'))


@app.route('/log-out')
def logout():
    logout_user()
    return redirect(url_for('index'))
