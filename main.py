




from fastapi import FastAPI , Depends
from sqlalchemy.orm import Session
from database import get_db
from model import User
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name : str
    email : str
    password : str

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

@app.get("/")  
def home():
    return {"message": "FastAPI is running"}

@app.post("/users/")
def create_user(user : UserCreate , db :Session = Depends (get_db)):
    new_user = User(name = user.name , email = user.email , password = user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return(new_user)

@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return {"error": "User not found"}
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return {"error": "User not found"}
    
    db_user.name = user.name
    db_user.email = user.email
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}")
def display_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    return db_user
