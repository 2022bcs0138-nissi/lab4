from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

model = joblib.load("model/model.pkl")

@app.post("/predict")
def predict(features: list):
    prediction = model.predict([features])[0]

    return {
        "name": "Nissi Veronika Y",
        "roll_no": "2022BCS0138",
        "wine_quality": int(round(prediction))
    }
