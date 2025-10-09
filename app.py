# To activate virtual environment:
# Set-ExecutionPolicy RemoteSigned –Scope Process
# env\Scripts\Activate
# flask run --debug

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    print("test")
    return render_template('index.html')

@app.route('/cookbook')
def cookbook():
    r = [ 
        {"src": "peppers2.jpg",
        "href": "/peppers",
        "name": "Cream Cheese Stuffed Peppers"},
        # Add star system
        # "rating": 4
        {"src": "cat.jpg",
        "href": "",
        "name": "Recipe Name"}
    ]
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

    return render_template('cookbook.html')
    

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
