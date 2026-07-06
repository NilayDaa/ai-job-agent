from fastapi import Header, HTTPException

from app.services.jwt_service import jwt_service

from app.repositories.user_repository import get_user_by_id


def get_current_user(
    authorization: str = Header(None)
):

    if authorization is None:
        raise HTTPException(
            status_code=401,
            detail="Missing authorization header"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header"
        )

    token = authorization.split(" ")[1]

    payload = jwt_service.verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = get_user_by_id(
        int(payload["sub"])
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user