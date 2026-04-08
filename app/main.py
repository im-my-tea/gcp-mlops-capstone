import pandas as pd
import numpy as np
import joblib
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 1. Setup & Path Management
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# 2. Load Artifacts 
print("Loading models into memory...")
try:
    scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
    model = joblib.load(os.path.join(MODEL_DIR, "neural_net_model.pkl")) 
except FileNotFoundError:
    raise RuntimeError("Model files not found! Did you run train.py?")

app = FastAPI(title="Breast Cancer Detection API", version="1.0")

# 3. Define Input Data Model (Matches the CSV columns exactly)
class PatientData(BaseModel):
    radius_mean: float
    texture_mean: float
    perimeter_mean: float
    area_mean: float
    smoothness_mean: float
    compactness_mean: float
    concavity_mean: float
    concave_points_mean: float
    symmetry_mean: float
    fractal_dimension_mean: float
    radius_se: float
    texture_se: float
    perimeter_se: float
    area_se: float
    smoothness_se: float
    compactness_se: float
    concavity_se: float
    concave_points_se: float
    symmetry_se: float
    fractal_dimension_se: float
    radius_worst: float
    texture_worst: float
    perimeter_worst: float
    area_worst: float
    smoothness_worst: float
    compactness_worst: float
    concavity_worst: float
    concave_points_worst: float
    symmetry_worst: float
    fractal_dimension_worst: float

@app.get("/")
def home():
    return {"status": "System Operational", "model": "Neural Network v1"}

@app.post("/predict")
def predict_cancer(data: PatientData):
    try:
        # 1. Convert Input JSON -> DataFrame 
        input_data = pd.DataFrame([data.dict()])
        
        # The model expects spaces in these specific names
        rename_map = {
            "concave_points_mean": "concave points_mean",
            "concave_points_se": "concave points_se",
            "concave_points_worst": "concave points_worst"
        }
        input_data = input_data.rename(columns=rename_map)

        # 2. Scale the Data (Crucial! Model fails without this)
        scaled_data = scaler.transform(input_data)
        
        # 3. Predict
        prediction = model.predict(scaled_data)[0] # Returns 0 or 1
        probability = model.predict_proba(scaled_data)[0].max() # Confidence score
        
        # 4. Map Result
        diagnosis = "Malignant" if prediction == 1 else "Benign"
        
        return {
            "diagnosis": diagnosis,
            "confidence": f"{probability * 100:.2f}%",
            "model_used": "MLP Neural Network"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
