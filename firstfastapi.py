from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from pymongo import MongoClient
from bson import ObjectId

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
users_collection = db["users"]

# FastAPI app
app = FastAPI(title="User CRUD API",
                description="API to create, read, update, and delete users",
                version="1.0.0")

# Pydantic models
class User(BaseModel):
    name: str = Field(..., description="Full name of the user")
    email: str = Field(..., description="User email address")
    age: int = Field(..., gt=0, description="User age")

class UserResponse(User):
    id: str

# Helper function to convert ObjectId to str
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "age": user["age"]
    }

# ----------------- CRUD Routes -----------------

# Create user
@app.post("/users", response_model=UserResponse)
def create_user(user: User):
    result = users_collection.insert_one(user.dict())
    new_user = users_collection.find_one({"_id": result.inserted_id})
    return user_helper(new_user)

# Read all users
@app.get("/users", response_model=List[UserResponse])
def get_users():
    users = [user_helper(u) for u in users_collection.find()]
    return users

# Read single user
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_helper(user)

# Update user
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user: User):
    result = users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = users_collection.find_one({"_id": ObjectId(user_id)})
    return user_helper(updated_user)

# Delete user
@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}

