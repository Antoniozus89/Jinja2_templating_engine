from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import TemplateResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()


templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id: int
    username: str
    age: int


users: List[User] = []


@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get('/users/{user_id}')
async def get_user(request: Request, user_id: int = Path(..., ge=1)):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})

    raise HTTPException(status_code=404, detail="User was not found")



@app.post('/user/{username}/{age}', response_model=User)
async def add_user(
        username: str = Path(..., min_length=5, max_length=20, description="Enter username", example="UrbanUser"),
        age: int = Path(..., ge=18, le=120, description="Enter age", example=24)
):
    new_id = (users[-1].id + 1) if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user



@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def update_user(
        user_id: int = Path(..., ge=1),
        username: str = Path(..., min_length=5, max_length=20),
        age: int = Path(..., ge=18, le=120)
):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user

    raise HTTPException(status_code=404, detail="User was not found")



@app.delete('/user/{user_id}', response_model=User)
async def delete_user(
        user_id: int = Path(..., ge=1)
):
    for index, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(index)
            return deleted_user

    raise HTTPException(status_code=404, detail="User was not found")

