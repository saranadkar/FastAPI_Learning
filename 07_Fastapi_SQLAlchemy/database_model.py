from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "Product"
    
    Id = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    Price = Column(Float)
    Quantity = Column(Integer)
    