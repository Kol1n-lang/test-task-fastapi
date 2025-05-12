from app.core.configs import all_settings
from app.core.schemas.repo_protocols import AuthRepoProtocol
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.configs.constants import ACCESS_TOKEN, REFRESH_TOKEN


class JWTService:
    def __init__(self, auth_repo: AuthRepoProtocol):
        self._auth_repo = auth_repo

    def create_access_refresh_tokens(self, data: dict) -> dict:
        to_encode_access = data.copy()
        to_encode_refresh = data.copy()
        expire_access = datetime.now(timezone.utc) + timedelta(
            minutes=all_settings.jwt.access_token_expire_minutes
        )
        expire_refresh = datetime.now(timezone.utc) + timedelta(
            minutes=all_settings.jwt.refresh_token_expire_minutes
        )
        to_encode_access.update({"exp": expire_access})
        to_encode_refresh.update({"exp": expire_refresh})
        to_encode_access.update({"type": ACCESS_TOKEN})
        to_encode_refresh.update({"type": REFRESH_TOKEN})
        auth_data = self.get_auth_data()
        access_jwt = jwt.encode(
            to_encode_access, auth_data["secret_key"], algorithm=auth_data["algorithm"]
        )
        refresh_jwt = jwt.encode(
            to_encode_refresh, auth_data["secret_key"], algorithm=auth_data["algorithm"]
        )
        return {"access_token": access_jwt, "refresh_token": refresh_jwt}

    def get_auth_data(self) -> dict:
        return {
            "secret_key": all_settings.jwt.secret_key,
            "algorithm": all_settings.jwt.algorithm,
        }

    def get_info_from_token(self, token: str) -> dict:
        token = token.split(" ", 1)[1]
        token_payload: dict = jwt.decode(
            token, all_settings.jwt.secret_key, algorithms=all_settings.jwt.algorithm
        )
        token_username = token_payload.get("username")
        token_email = token_payload.get("email")
        return {"username": token_username, "email": token_email}
