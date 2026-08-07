# fastapi with SQL integration

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base


from pydantic import BaseModel
from typing import Optional, List


app = FastAPI(title = "integration with sql")

# Database setup 
# Create engine
engine = create_engine("sqlite:///users.db", connect_args={"check_same_thread":False}) 
# Engine = the connection manager.
# It knows HOW and WHERE to connect to the database.
# The URL specifies the database.
# connect_args are optional driver-specific options.


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 
# SessionLocal = a factory that creates Session objects.
# bind=engine tells every Session which Engine to use.
# autocommit and autoflush are optional behavior settings.

Base = declarative_base()
# Base = the blueprint (parent class) for every ORM model.
# Every table inherits from Base.
# SQLAlchemy later inspects Base to discover all models.






# database model
class User(Base):
    __tablename__ ="users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role = Column(String(100), nullable=False)

Base.metadata.create_all(engine)

#Pydantic Models (Datacalss)
class UserCreate(BaseModel):
    name:str
    email:str
    role:str

class UserResponse(BaseModel):
    id:int
    name:str
    email:str
    role:str

    class Config:
        from_attribute = True

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


#endpoints
@app.get("/")
def root():
    return {"message":"it works, I think"}

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id:int, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User no exisitng")
    return user

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db:Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=401, detail="User exisiting bro")

    #create new user
    new_user = User(**user.dict()) #giving it everything it needs
    db.add(new_user)
    db.commit()  # if you dont commit python is not speaking to db
    db.refresh(new_user)
    return new_user

# endpoint to update user

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id:int,user:UserCreate, db:Session = Depends(get_db)):
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="No existe tu pince usuario")

    for field, value in user.dict().items():
        setattr(user_db,field,value)

    db.commit()
    db.refresh(user_db)
    return user_db

# delete a user

@app.delete("users/{user_id}")
def delete_user(user_id:int, db:Session = Depends(get_db)):
    user_del = db.query(User).filter(User.id == user_id).first()
    if not user_del:
        raise HTTPException(status_code=404, detail="estimado cliente, el usuario que usted busca no se encuentra disponible, gracias")
    
    db.delete(user_del)
    db.commit()
    return {"message":"successefully deleted the requested user"}




