from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from pathlib import Path as filepath
import json


router = APIRouter(
    prefix="/patients",
    tags=["patient"]
)

BASE_DIR = filepath(__file__).parent

class Address(BaseModel):
    city: str
    state: str
    pincode: int
    

class Patient(BaseModel):
    id:str
    name: str
    age: int
    address: Address
    

def load_data():
    with open(BASE_DIR/"Patient.json","r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open(BASE_DIR/"Patient.json","w") as f:
        json.dump(data,f)

@router.get("/")
def view():
    data = load_data()
    return data

@router.get("/{patient_id}")
def view_patient(patient_id: str):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404,detail="Patient not found")