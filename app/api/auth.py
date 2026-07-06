from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.repositories.user_repository import (
    create_user,
    username_exists,
    email_exists,
    get_user_by_email,
)

from app.services.auth_service import auth_service
from app.services.jwt_service import jwt_service
from fastapi import Depends
from app.core.security import get_current_user

router = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(request: RegisterRequest):

    # Check username
    if username_exists(request.username):
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Check email
    if email_exists(request.email):
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Hash password
    password_hash = auth_service.hash_password(
        request.password
    )

    # Save user
    user_id = create_user(
        request.username,
        request.email,
        password_hash
    )

    return {
        "message": "User registered successfully",
        "user_id": user_id
    }

@router.post("/login")
def login(request: LoginRequest):

    user = get_user_by_email(request.email)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not auth_service.verify_password(
        request.password,
        user["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = jwt_service.create_access_token(
        user["id"]
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return current_user