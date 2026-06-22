from fastapi import FastAPI,Path
import json
from pathlib import Path

app = FastAPI()

BASE_DIR = Path("D:/FastAPI_Learning/02_HTTP_methods")

def load_data():
    with open(BASE_DIR/'patient.json','r') as f:
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return {"message":"Patient management syatem API."}

@app.get("/about")
def about():
    return{"message":"A functional API to manage your patient records."}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="ID of the patient in DB",example ="P001" )):
    # load the data
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    return {"error":"patient not found"}