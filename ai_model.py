import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import json

with open("carbon_data.json", "r") as file:
    data = json.load(file)

df = pd.DataFrame(data)

features = ["Energy Usage (MWh)", "Fuel Consumption (L)", "Industrial Output (tons)",
            "Waste Generated (tons)", "Transport Distance (km)"]

target_emissions = "Total Emissions (kg CO₂)"
target_credits = "Carbon Credits Required"

X = df[features]
y_emissions = df[target_emissions]
y_credits = df[target_credits]

X_train, X_test, y_train_emissions, y_test_emissions = train_test_split(X, y_emissions, test_size=0.2, random_state=42)
X_train, X_test, y_train_credits, y_test_credits = train_test_split(X, y_credits, test_size=0.2, random_state=42)

model_emissions = LinearRegression()
model_credits = LinearRegression()

model_emissions.fit(X_train, y_train_emissions)
model_credits.fit(X_train, y_train_credits)

def predict_emissions(input_data):
    prediction = model_emissions.predict(np.array([input_data]))
    return round(prediction[0], 2)

def predict_credits(input_data):
    prediction = model_credits.predict(np.array([input_data]))
    return round(prediction[0], 2)
