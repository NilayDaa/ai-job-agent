from datetime import datetime, timedelta

from jose import jwt

SECRET_KEY = "change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class JWTService:

    def create_access_token(self, user_id: int):

        payload = {
            "sub": str(user_id),
            "exp": datetime.utcnow() + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        }

        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM
        )


jwt_service = JWTService()