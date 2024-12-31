from locust import HttpUser, task, between
import random
import argparse
import os

# List of user agents to randomize requests
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
]

# List of pages to randomize requests
PAGES = ["/", "/about", "/products", "/faq", "/contact"]

class MyUser(HttpUser):
    # Wait time between requests (1 to 5 seconds)
    wait_time = between(1, 5)

    @task
    def random_page(self):
        # Randomly choose a user agent
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br"
        }
        # Randomly choose a page to visit
        page = random.choice(PAGES)
        self.client.get(page, headers=headers)

    @task
    def submit_form(self):
        # Simulate a form submission with realistic data
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br"
        }
        data = {
            "name": "Test User",
            "email": f"test{random.randint(1000, 9999)}@example.com",
            "message": "This is a test message."
        }
        self.client.post("/submit", data=data, headers=headers)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run Locust load tests with custom parameters.")
    parser.add_argument("-u", "--users", type=int, default=10, help="Number of users to simulate.")
    parser.add_argument("-r", "--rate", type=int, default=2, help="User spawn rate (users per second).")
    parser.add_argument("-t", "--time", type=str, default="1m", help="Test duration (e.g., 1m, 30s).")
    parser.add_argument("-H", "--host", type=str, required=True, help="Target host for the load test.")
    
    args = parser.parse_args()
    
    # Build the Locust command
    locust_command = (
        f"locust --headless -u {args.users} -r {args.rate} -t {args.time} -H {args.host}"
    )
    
    # Run the Locust command
    os.system(locust_command)
