from httpx import AsyncClient

test_user = {"username": "string", "email": "user@example.com", "password": "string"}


async def test_register(client: AsyncClient) -> None:
    response = await client.post("/api/v1/auth/register", json=test_user)
    assert response.status_code == 200
    assert type(response.json()) is str


async def test_login(client: AsyncClient) -> None:
    response = await client.post("/api/v1/auth/login", json=test_user)
    assert response.status_code == 200
    access_token, refresh_token = (
        response.json()["access_token"],
        response.json()["refresh_token"],
    )
    print(access_token, refresh_token)
    assert access_token is not None and refresh_token is not None
    assert type(access_token) is str and type(refresh_token) is str
