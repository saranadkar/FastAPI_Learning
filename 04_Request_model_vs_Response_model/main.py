from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, computed_field,field_validator
from typing import Annotated, Literal 
from pathlib import Path as filepath
import json
from fastapi.responses import JSONResponse

app = FastAPI()

BASE_DIR = filepath(__file__).parent

#Request Model  → What API receives
#Response Model → What API sends

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City where the patient lives")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[
        Literal["male", "female", "other"],
        Field(..., description="Gender of the patient")
    ]
    height: Annotated[float, Field(..., gt=0)]
    weight: Annotated[float, Field(..., gt=0)]
    
    
class PatientResponse(BaseModel):
        id: Annotated[str, Field(..., description="ID of the patient", examples=["P001"])]
        name: Annotated[str, Field(..., description="Name of the patient")]
        
        ###use of field validator
        @field_validator("name")
        @classmethod
        def validate_name(cls, value):
            if not value.isalpha():
                raise ValueError("Name should contain only letters")

            return value
        
        city: Annotated[str, Field(..., description="City where the patient lives")]
        age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
        gender: Annotated[
        Literal["male", "female", "other"],
        Field(..., description="Gender of the patient")
    ]
        height: Annotated[float, Field(..., gt=0)]
        weight: Annotated[float, Field(..., gt=0)]
        
        @computed_field
        @property
        def bmi(self) ->float:
            bmi = round(self.weight / (self.height ** 2), 2)
            return bmi
        
        @computed_field
        @property
        def verdict(self) -> str:
            if self.bmi < 18.5:
                return "Underweight"

            elif self.bmi < 25:
                return "Normal"

            elif self.bmi < 30:
                return "Overweight"

            else:
                return "Obese"
    
def load_data():
    with open(BASE_DIR/"Patient.json","r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open(BASE_DIR/"Patient.json","w") as f:
        json.dump(data,f)
            
    
@app.get("/patient/{patient_id}", response_model=PatientResponse)
def view_patient(patient_id: str):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404,detail="Patient not found")

@app.post("/create")
def create_patient(patient:Patient):
    data = load_data()
    
    if patient.id in data:
        raise HTTPException(status_code=400,detail="patient already exists.")
    
    #add new patient in DB
    data[patient.id] = patient.model_dump()   # dumps is used to convert into dictionary
    
    #save into json file
    save_data(data)
    
    return JSONResponse(status_code=201, content={'message':'patient created successfully'})