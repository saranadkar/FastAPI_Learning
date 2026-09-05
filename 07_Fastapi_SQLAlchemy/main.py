from fastapi import FastAPI, Depends
from model import Product
from database import session,engine
import database_model

app = FastAPI()

database_model.Base.metadata.create_all(bind = engine)

@app.get("/")
def greet():
    return "Welcome."

products = [
    Product(Id=1, Name="Phone", Price=699.99, Quantity=50),
    Product(Id=2, Name="Laptop", Price=999.99, Quantity=30),
    Product(Id=3, Name="Pen", Price=1.99, Quantity=100),
    Product(Id=4, Name="Table", Price=199.99, Quantity=20),
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    
    count = db.query(database_model.Product).count()
    
    if count == 0:
        for product in products:
            db.add(database_model.Product(**product.model_dump()))
            
        db.commit()

init_db()

@app.get("/product")
def get_all_product(db  = Depends(get_db)):
    
    db_products = db.query(database_model.Product).all()

    return db_products

@app.get("/product/{Id}")
def get_product_by_Id(Id:int, db = Depends(get_db)):
    db_products = db.query(database_model.Product).filter(database_model.Product.Id == Id).first()
    if db_products:
        return db_products
    return "Product not found"

@app.post("/product")
def add_product(product:Product, db = Depends(get_db)):
    db.add(database_model.Product(**product.model_dump()))
    
    db.commit()
    return product

@app.put("/product")
def update_product(Id:int, product:Product, db = Depends(get_db)):
    
    db_product = db.query(database_model.Product).filter(database_model.Product.Id == Id).first()
    
    if db_product:
        db_product.Name = product.Name
        db_product.Quantity = product.Quantity
        db_product.Price = product.Price
        db.commit()
        return "Product Updated."
        
    else:
        return "No product found"
    
@app.delete("/product")
def delete_product(Id:int, db = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.Id == Id).first()
    
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Succesfully deleted."
        
    else:
        return "Product not found"