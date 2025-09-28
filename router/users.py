from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from user_jwt import create_token


login_router = APIRouter()


class User(BaseModel):
    email: str
    password: str


@login_router.post('/login', tags=["Authentication"])
def login(user: User):
    if user.email == "pampa@mail.com" and user.password == "1234":
        token:str = create_token(user.dict())
    return JSONResponse(content=token)