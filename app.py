from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model
with open('model/model_calories.pkl', 'rb') as f:
    model_calories = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    age = int(request.form['age'])
    gender = int(request.form['gender'])  # 0 for Male, 1 for Female
    height = float(request.form['height'])
    weight = float(request.form['weight'])
    meal_frequency = int(request.form['meal_frequency'])
    exercise_level = int(request.form['exercise_level'])
    
    # Calculate BMR
    if gender == 0:  # Male
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:  # Female
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    
    # Calculate Daily Caloric Needs based on activity level
    activity_multipliers = [1.2, 1.375, 1.55, 1.725, 1.9]
    daily_caloric_needs = bmr * activity_multipliers[exercise_level]

    # Calculate Macronutrient Distribution
    protein = 0.2 * daily_caloric_needs / 4  # 20% of calories from protein
    carbs = 0.5 * daily_caloric_needs / 4    # 50% of calories from carbs
    fats = 0.3 * daily_caloric_needs / 9     # 30% of calories from fats

    # Updated Hydration Advice
    hydration = 2.5  # Default to 2.5 liters
    if exercise_level > 0:  # If active, add extra water
        hydration += exercise_level * 0.5  # Add 0.5L per level of activity

    # Meal Plan Suggestions based on realistic distributions
    breakfast_carbs = carbs * 0.25
    lunch_carbs = carbs * 0.35
    dinner_carbs = carbs * 0.40
    
    breakfast_protein = protein * 0.25
    lunch_protein = protein * 0.35
    dinner_protein = protein * 0.40
    
    breakfast_fats = fats * 0.25
    lunch_fats = fats * 0.35
    dinner_fats = fats * 0.40

    meal_plan = {
        "Breakfast": f"{int(breakfast_carbs)}g carbs, {int(breakfast_protein)}g protein, {int(breakfast_fats)}g fats",
        "Lunch": f"{int(lunch_carbs)}g carbs, {int(lunch_protein)}g protein, {int(lunch_fats)}g fats",
        "Dinner": f"{int(dinner_carbs)}g carbs, {int(dinner_protein)}g protein, {int(dinner_fats)}g fats",
    } 

    # Render the results
    return render_template('result.html',
                           calories=daily_caloric_needs,
                           protein=protein,
                           carbs=carbs,
                           fats=fats,
                           hydration=hydration,
                           meal_plan=meal_plan)

# BMI Calculator page
@app.route('/bmi_calculator', methods=['GET', 'POST'])
def bmi_calculator():
    bmi = None
    category = None
    if request.method == 'POST':
        height = float(request.form['height'])  # height in meters
        weight = float(request.form['weight'])   # weight in kg
        
         # Calculate BMI
        # If height is in centimeters, convert it to meters
        height_m = height / 100 if height > 3 else height  # Assuming height > 3 is in meters

        bmi = round(weight / (height_m ** 2), 2)  # Round to 2 decimal places
        
        # Determine the category
        if bmi < 18.5:
            category = 'Underweight'
        elif bmi < 24.9:
            category = 'Normal weight'
        elif bmi < 29.9:
            category = 'Overweight'
        else:
            category = 'Obesity'
    
    return render_template('bmi_calculator.html', bmi=bmi, category=category)


# Healthy Diets page
@app.route('/healthy_diets')
def healthy_diets():
    return render_template('healthy_diets.html')

# Exercise Plans page
@app.route('/exercise_plans')
def exercise_plans():
    return render_template('exercise_plans.html')

# Fit Yoga page
@app.route('/fit_yoga_hit_yoga')
def fit_yoga_hit_yoga():
    return render_template('fit_yoga_hit_yoga.html')

# Homepage
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

# Homepage
@app.route('/healthy_calories')
def healthy_calories():
    return render_template('healthy_calories.html')


if __name__ == '__main__':
    app.run(debug=True)
