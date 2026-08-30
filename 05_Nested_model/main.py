from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Address(BaseModel):
    city: str
    state: str
    pincode: int


class Patient(BaseModel):
    name: str
    age: int
    address: Address


@app.post("/patient")
def create_patient(patient: Patient):
    return patient