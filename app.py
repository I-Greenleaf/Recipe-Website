from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cookbook')
def cookbook():
    return render_template('cookbook.html')

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

