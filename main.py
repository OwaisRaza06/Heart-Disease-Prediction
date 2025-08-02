from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, computed_field, Field
from typing import Annotated, List, Optional, Literal
import pandas as pd
import pickle
from fastapi.responses import JSONResponse
from mangum import Mangum

with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

class Person(BaseModel):
    male: Annotated[int, Field(..., title='Whether the person is male or female')]
    age: Annotated[int, Field(..., title='Age of the person')]
    education: Annotated[int, Field(..., title='education of the person')]
    currentSmoker: Annotated[int, Field(..., title='Is the person smoker')]
    cigsPerDay:Annotated[int, Field(..., title='How many cigarettes a person consume per day')]
    BPMeds: Annotated[int, Field(..., title='Number of blood pressure medicines person is consuming')]
    prevalentStroke: Annotated[int, Field(..., title='Does the patient had stroke previously')]
    prevalentHyp: Annotated[int, Field(..., title='Whether the person is male or female')]
    diabetes: Annotated[int, Field(..., title='Is patient diabetic')]
    totChol: Annotated[float, Field(..., title='Cholestrol level')]
    sysBP: Annotated[int, Field(..., title='Systolic blood pressure')]
    diaBP: Annotated[int, Field(..., title='Disystolic blood pressure')]
    weight: Annotated[float, Field(..., title='Weight of person')]
    height: Annotated[float, Field(..., title='Height of person')]
    heartRate: Annotated[float, Field(..., title='Heart rate of person')]
    glucose: Annotated[float, Field(..., title='Glucose level of person')]

    @computed_field
    @property
    def BMI(self) -> float:
         return self.weight/self.height**2

app = FastAPI()

handler = Mangum(app)

@app.get("/")
def health():
    return{'mesasge': 'heart disease api is working'}

@app.post("/predict")
def predict(data: Person):
    input = pd.DataFrame([{
        'male': data.male,
        'age': data.age,
        'education': data.education,
        'currentSmoker': data.currentSmoker,
        'cigsPerDay':data.cigsPerDay,
        'BPMeds': data.BPMeds,
        'prevalentStroke': data.prevalentStroke,
        'prevalentHyp': data.prevalentHyp,
        'diabetes': data.diabetes,
        'totChol': data.totChol,
        'sysBP': data.sysBP,
        'diaBP': data.diaBP,
        'BMI': data.BMI,
        'heartRate': data.heartRate,
        'glucose': data.glucose
    }])
    
    prediction = model.predict(input)

    return JSONResponse(status_code=200, content={'chances of Ten year CHD': prediction.item()})