from httpx import AsyncClient

test_user = {
    "username": "string",
    "email": "user@example.com",
    "password": "string"
}

transaction = {
    "amount": 1,
    "bill_id": "5e5cd451-a5b2-4924-98bc-384c32ddc474" # insert uuid of bill
}
async def test_create_bill(client: AsyncClient) -> None:
    token = (await client.post("/api/v1/auth/login", json=test_user)).json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    response = await client.post("/api/v1/bank/create-bill")
    assert response.status_code == 200
    response = await client.post("/api/v1/bank/create-bill")
    assert response.status_code == 200

async def test_create_transaction(client: AsyncClient) -> None:
    token = (await client.post("/api/v1/auth/login", json=test_user)).json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    response = await client.post("/api/v1/bank/payment", json=transaction)
    assert response.status_code == 200

async def test_get_bill(client: AsyncClient) -> None:
    token = (await client.post("/api/v1/auth/login", json=test_user)).json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    response = await client.get(f"/api/v1/bank/get-bills/{transaction['bill_id']}")
    assert response.status_code == 200
    assert response.json()["balance"] == transaction["amount"]
    assert response.json()["id"] == transaction["bill_id"]
    assert len(response.json()["bill_transactions"]) == 1

