from typing import List
from fastapi import APIRouter, status, Request, Body, HTTPException, Response
from fastapi.encoders import jsonable_encoder

from models.User import UserSchema, UpdateUserSchema

router = APIRouter()


@router.get("/")
async def hello():
    return {"message": "Hello World"}


@router.get("/users", response_description="All users", response_model=List[UserSchema])
def all_users(request: Request):
    users = list(request.app.database["users"].find(limit=100))
    return users


@router.post("/user/add", response_description="Create new user", status_code=status.HTTP_201_CREATED,
             response_model=UserSchema)
def create_user(request: Request, user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = request.app.database["users"].insert_one(user)
    created_user = request.app.database["users"].find_one(
        {"_id": new_user.inserted_id}
    )

    return created_user


@router.put("/user/{id}", response_description="Update a user", response_model=UpdateUserSchema)
def update_user(id: str, request: Request, user: UpdateUserSchema = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}
    if len(user) >= 1:
        update_result = request.app.database["users"].update_one(
            {"_id": id}, {"$set": user}
        )
        if update_result.modified_count == 0:
            return "User not found"
    if (
            exist_user := request.app.database["users"].find_one({"_id": id})
    ) is not None:
        return exist_user

    return "User not found"


@router.delete("/user/{id}", response_description="Delete a user")
def delete_user(id: str, request: Request, response: Response):
    delete_result = request.app.database["users"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return "User not found"
