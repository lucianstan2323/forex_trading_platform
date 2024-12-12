import pytest

class TestOrders:
    @pytest.mark.asyncio
    async def test_get_all_orders(self, client, base_url):
        url = f"{base_url}/orders/"
        response = client.get(url)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @pytest.mark.asyncio
    async def test_create_order(self, client, base_url):
        url = f"{base_url}/orders/"
        payload = {"stoks": "EURUSD", "quantity": 100}
        response = client.post(url, json=payload)
        assert response.status_code == 201
        assert response.json()["stoks"] == "EURUSD"

    @pytest.mark.asyncio
    async def test_create_order_invalid(self, client, base_url):
        url = f"{base_url}/orders/"
        payload = {"stoks": "EURUSD"}  # Missing quantity
        response = client.post(url, json=payload)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_get_specific_order(self, client, base_url):
        url = f"{base_url}/orders/"
        # Create order first
        payload = {"stoks": "GBPUSD", "quantity": 50}
        post_response = client.post(url, json=payload)
        order_id = post_response.json()["id"]

        # Get the specific order
        url = f"{base_url}/orders/{order_id}"
        response = client.get(url)
        assert response.status_code == 200
        assert response.json()["id"] == order_id

    @pytest.mark.asyncio
    async def test_get_nonexistent_order(self, client, base_url):
        url = f"{base_url}/orders/nonexistent"
        response = client.get(url)
        assert response.status_code == 404
