import bcrypt


class AuthService:

    def hash_password(self, password: str) -> str:
        hashed = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )
        return hashed.decode("utf-8")

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )


auth_service = AuthService()