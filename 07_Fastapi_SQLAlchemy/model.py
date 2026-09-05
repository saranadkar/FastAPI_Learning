from pydantic import BaseModel

class Product(BaseModel):
    Id: int
    Name: str
    Price: float
    Quantity: int
    