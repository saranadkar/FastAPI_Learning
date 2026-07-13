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
