import pytest
from locust import HttpUser, task, between, run_single_user
from locust.env import Environment
from locust.runners import MasterRunner
from locust import events
import time

# Define the load test behavior in a class
class OrderLoadTest(HttpUser):
    #wait_time = between(0.01, 0.02)

    @task(1)
    def create_order(self):
        order_data = {
            "stoks": random.choice(["EURLOC", "GBPLOC", "USDLOC"]),
            "quantity": random.randint(1, 100)
        }
        response = self.client.post("/orders/", json=order_data)

        assert response.status_code == 201, f"Failed to create order: {response.status_code}"

        order_id = response.json()['id']
        print(f"Order created with ID: {order_id}")
        self.order_ids.append(order_id)  # Store the created order ID for later

# Define a pytest fixture for setting up the environment and runner
@pytest.fixture(scope="function")
def locust_environment():
    # Set up Locust environment
    environment = Environment(user_classes=[OrderLoadTest])

    # Configure the runner to run the load test
    environment.create_local_runner()

    # Start the runner with 100 users instantly
    environment.runner.start(100, spawn_rate=100)  # 100 users with a spawn rate of 100 per second

    # Yield the environment so that the test can run
    yield environment

    # Wait for the test to complete and stop it after the test
    environment.runner.greenlet.join()

@pytest.mark.parametrize("num_users", [100])
def test_load(locust_environment, num_users):
    """
    Run Locust load test with 100 users (parameterized).
    """
    print(f"Running load test with {num_users} users.")
    
    # Run the load test programmatically
    locust_environment.runner.greenlet.join()  # Wait for the test to finish

    # Optionally, you can verify stats here or add assertions to check the results
    assert locust_environment.runner.stats.total.num_requests > 0, "No requests were made."
    print(f"Total requests made: {locust_environment.runner.stats.total.num_requests}")