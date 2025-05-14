from typing import Protocol


class JWTServiceProtocol(Protocol):

    def create_access_refresh_tokens(self, data: dict) -> dict:
        """Create a JWT token"""
        pass

    def get_auth_data(self) -> dict:
        """Get auth data"""
        pass

    def get_info_from_token(self, token: str | None) -> dict:
        """Get info from token"""
        pass
