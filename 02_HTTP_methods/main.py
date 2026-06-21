from fastapi import FastAPI
import json
from pathlib import Path

app = FastAPI()

BASE_DIR = Path("D:/FastAPI_Learning/02_HTTP_methods")

def load_load():
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
    data = load_load()
    return data