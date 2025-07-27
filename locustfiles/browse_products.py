from locust import HttpUser, task, between
from random import randint


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task(2)
    def view_products(self):
        """
        Simulates browsing all products under a specific collection.
        The collection_id is randomly chosen between 2 and 6.
        This sends a GET request to the endpoint /store/product/?collection_id={id}.
        Example: Viewing all Apple products (iPhone, MacBook, etc.).
        """

        collection_id = randint(2, 6)
        self.client.get(
            f"/store/product/?collection_id={collection_id}", name="store/products/"
        )

    @task(4)
    def view_product(self):
        """
        Simulates viewing the details of a single product.
        The product_id is randomly chosen between 1 and 1000.
        Sends a GET request to /store/product/{id} to fetch product details like title, slug, price, etc.
        """

        product_id = randint(1, 1000)
        self.client.get(f"/store/product/{product_id}", name="/store/products/:id")

    @task(1)
    def add_to_cart(self):
        """
        Simulates adding a product to the shopping cart.
        Uses the previously created cart_id from on_start.
        A random product_id between 1 and 10 is selected, and quantity is set to 1.
        Sends a POST request to /store/carts/{cart_id}/items/ with JSON body.
        """

        product_id = randint(1, 10)
        self.client.post(
            f"/store/carts/{self.cart_id}/items/",
            name="/store/carts/items",
            json={"product_id": product_id, "quantity": 1},
        )

    @task
    def say_hello(self):
        self.client.get("/playground/hello/")

    def on_start(self):
        """
        This method is called when a simulated user starts.
        It sends a POST request to create a new shopping cart.
        The response JSON contains a UUID (cart ID), which is saved to self.cart_id
        so it can be reused in subsequent requests (like adding items to the cart).
        """

        response = self.client.post("/store/carts/")
        result = response.json()
        self.cart_id = result["id"]
