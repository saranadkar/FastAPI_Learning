"""
==============================================================
FastAPI Practice - Patient Management API

This file contains my solutions to FastAPI practice questions.

Topics Covered:
✔ Path Parameters
✔ Query Parameters
✔ CRUD Operations
✔ Pydantic Models
✔ Data Validation
✔ HTTPException
✔ JSON File Handling

Author: Sara Nadkar
==============================================================
"""

from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pathlib import Path as filepath
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

app = FastAPI()

# ==========================================================
# Patient Model
# ==========================================================
# This model validates the data received while creating
# a new patient.
# BMI and Verdict are computed automatically.
# ==========================================================

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

    @computed_field
    @property
    def bmi(self) -> float:
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


BASE_DIR = filepath(__file__).parent


# ==========================================================
# Helper Functions
# ==========================================================
# load_data()  -> Reads patient data from patient.json
# save_data()  -> Saves updated patient data to patient.json
# ==========================================================

def load_data():
    with open(BASE_DIR / "patient.json", "r") as f:
        data = json.load(f)
    return data


def save_data(data):
    with open(BASE_DIR / "patient.json", "w") as f:
        json.dump(data, f)


# ==========================================================
# View All Patients
#
# Endpoint:
# GET /view
#
# Objective:
# Return all patient records stored in the JSON file.
# ==========================================================

@app.get("/view")
def view():
    data = load_data()
    return data


# ==========================================================
# Level 1 - Warm-up
# ==========================================================


# ----------------------------------------------------------
# Question 1
#
# Endpoint:
# GET /patients/city/{city_name}
#
# Objective:
# Return all patients belonging to the given city.
#
# Requirements:
# ✔ Accept city as a Path Parameter
# ✔ Ignore upper/lower case while searching
# ✔ Return HTTPException(404) if no patients are found
# ----------------------------------------------------------

@app.get("/patient/city/{city_name}")
def patient_city(city_name: str):

    patients = []

    data = load_data()

    for patient in data.values():

        if patient["city"].lower() == city_name.lower():
            patients.append(patient)

    if not patients:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patients


# ----------------------------------------------------------
# Question 2
#
# Endpoint:
# GET /count
#
# Objective:
# Return the total number of patients present
# in the database.
#
# Expected Output:
#
# {
#     "total_patients": 8
# }
# ----------------------------------------------------------

@app.get("/count")
def patient_count():

    data = load_data()

    total = len(data)

    return {
        "total_patients": total
    }



# Q3. GET /patient/oldest
# Create an endpoint that returns the oldest patient
# from the database.
@app.get('/patient/oldest')
def get_oldest_patient():
    
    data = load_data()
    
    oldest =max(data.items(),key=lambda patient: patient["age"])
    return oldest



# Q4. GET /patient/youngest
# Create an endpoint that returns the youngest patient
# from the database.
@app.get('/patient/youngest')
def get_youngest_patient():
    
    data = load_data()
    
    oldest =min(data.items(),key=lambda patient: patient["age"])
    return oldest



# Q5. GET /search?name=sara
# Create an endpoint that searches patients by name using
# a query parameter. The search should ignore uppercase
# and lowercase characters.
@app.get('/search')
def get_patient_by_name(name: str= Query(...,description="Enter patient name")):
    
    data = load_data()
    
    result=[]
    
    for patient in data.values():
        if name.strip().lower() in patient["name"].strip().lower():
            result.append(patient)
            
    if not result:
        raise HTTPException(status_code=404,detail="patient not found")
        
    return result



# Q6. GET /patients?age=30
# Return all patients whose age is greater than the given age.
# Example:
# Request: GET /patients?age=30
# Response: List of all patients with age > 30.
@app.get('/patients')
def get_patient_by_age(age: int=Query(...,description="Enter age of patient")):
    
    result = []
    
    data = load_data()
    
    for patient in data.values():
        if patient["age"]>age:
            result.append(patient)

    if not result:
        raise HTTPException(status_code=404,detail="patient not found")
    
    return result


# Q7. GET /patients/verdict?category=Normal
# Return all patients belonging to the specified BMI category.
# Categories:
# - Underweight
# - Normal
# - Overweight
# - Obese
# Example:
# Request: GET /patients/verdict?category=Normal
# Response: List of all patients whose BMI category is "Normal".
@app.get('/patients/verdict')
def get_patient_by_bmi_category(category: str=Query(...,description="Enter category of patient")):
    
    result = []
    
    data = load_data()
    
    for patient in data.values():
        if patient["verdict"].lower()==category.lower():
            result.append(patient)

    if not result:
        raise HTTPException(status_code=404,detail="patient not found")
    
    return result


# Q8. GET /patients/height?min_height=1.5&max_height=1.8
# Return all patients whose height falls within the given range (inclusive).
# Example:
# Request: GET /patients/height?min_height=1.5&max_height=1.8
# Response: List of all patients with height between 1.5 and 1.8 meters.
@app.get('/patients/height')
def get_patients_by_height(
    min_height:float=Query(...,description="Enter minimum height of patient"),
    max_height:float=Query(...,description="Enter maximum height of patient")):
    
    result = []
    
    data = load_data()
    
    for patient in data.values():
        if patient["height"]>=min_height and patient["height"]<=max_height:
            result.append(patient)
    
    if not result:
        raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )
    
    return result


# Q9. GET /patients?skip=0&limit=3
# Implement pagination.
# Return a limited number of patients after skipping the specified number of records.
# Example:
# Request: GET /patients?skip=2&limit=3
# Response: Returns 3 patients starting from index 2.
@app.get('/patients/pagination')
def get_patient_by_pagination(
    skip: int = Query(..., description="Number of records to skip"),
    limit: int = Query(..., description="Maximum number of records to return")
    ):
    
    data = load_data()
    
    # Convert dictionary values into a list
    patients=list(data.values())
    
    # Return patients after skipping 'skip' records
    result = patients[skip:skip+limit]
            
    
    if not result:
        raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )
    
    return result


# Q10. GET /patients/sort?sorted_by=age
# sorting endpoint to support multiple fields.
#
# Requirements:
# - Sort patients by any one of the following fields:
#   • age
#   • city
#   • name
#
# Example Requests:
# GET /patients/sort?sorted_by=age
# GET /patients/sort?sorted_by=city
# GET /patients/sort?sorted_by=name

@app.get('/patients/sort')
def sort_patients(sorted_by:str = Query(...,description="Sort patients by age, city, or name")):
    
    valid_fields=["age","city","name"]
    
    if sorted_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'select from given {valid_fields} fields')
    
    data = load_data()
    
    sorted_data = sorted(data.values(), key=lambda x:x[sorted_by])
    
    return sorted_data