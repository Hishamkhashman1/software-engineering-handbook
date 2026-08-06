# fastapi with SQL integration

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


from pydantic import BaseModel
from typing import Optional, List


app = FastAPI(title = "integration with sql")

# Database setup 
# Create engine
engine = create_engine("sqlite:///users.db", connect_args={"check_same_thread":False})
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()

# database model
class User(base):
    __tablename__ ="users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role = Column(String(100), nullable=False)

base.metadata.create_all(engine)

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
    db = session_local()

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

@app.put("/user/{user_id}", response_model=UserResponse)
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

@app.delete("user/{user_id}", response_model=UserResponse)
def delete_user(user_id:int, db:Session = Depends(get_db)):
    user_del = db.query(User).filter(User.id == user_id).first()
    if not user_del:
        raise HTTPException(status_code=404, detail="estimado cliente, el usuario que usted busca no se encuentra disponible, gracias")
    
    db.delete(user_del)
    db.commit()
    db.refresh(user_del)
    return {"message":"successefully deleted the requested user"}




