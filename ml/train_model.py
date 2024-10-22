import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# Load dataset
data = pd.read_csv('data/user_nutritional_data.csv')

# Features and target variables
X = data[['Gender', 'Age', 'Height', 'Weight', 'Daily meals frequency', 'Physical exercise']]
y_calories = data['Calories']

# Train-test split
X_train, X_test, y_train_calories, y_test_calories = train_test_split(X, y_calories, test_size=0.2, random_state=42)

# Train the model (Linear Regression as baseline)
model_calories = LinearRegression()
model_calories.fit(X_train, y_train_calories)

# Save the model
with open('model/model_calories.pkl', 'wb') as f:
    pickle.dump(model_calories, f)

print("Model training complete, and model saved as 'model_calories.pkl'")
