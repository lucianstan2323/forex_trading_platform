import pytest

class TestOrders:
    @pytest.mark.asyncio
    async def test_get_all_orders(self, client):
        response = await client.get("/orders/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @pytest.mark.asyncio
    async def test_create_order(self, client):
        payload = {"stoks": "EURUSD", "quantity": 100}
        response = await client.post("/orders/", json=payload)
        assert response.status_code == 201
        assert response.json()["stoks"] == "EURUSD"

    @pytest.mark.asyncio
    async def test_create_order_invalid(self, client):
        payload = {"stoks": "EURUSD"}  # Missing quantity
        response = await client.post("/orders/", json=payload)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_get_specific_order(self, client):
        # Create order first
        payload = {"stoks": "GBPUSD", "quantity": 50}
        post_response = await client.post("/orders/", json=payload)
        order_id = post_response.json()["id"]

        # Get the specific order
        response = await client.get(f"/orders/{order_id}")
        assert response.status_code == 200
        assert response.json()["id"] == order_id

    @pytest.mark.asyncio
    async def test_get_nonexistent_order(self, client):
        response = await client.get("/orders/nonexistent")
        assert response.status_code == 404
