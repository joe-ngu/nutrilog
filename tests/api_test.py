import random
import string
from fastapi import status


FOODS_API_ENDPOINT = "/api/v1/foods"
USERS_API_ENDPOINT = "/api/v1/users"


class TestFoodsAPI:
    """Test cases for the foods API"""

    async def test_create_food(self, client):
        green_egg = {
            "name": "egg",
            "quantity": 44,
            "fats": 6,
            "carbs": 0.5,
            "protein": 6,
        }
        response = await client.post(FOODS_API_ENDPOINT, json=green_egg)
        pk = response.json().get("pk")
        assert pk is not None

    async def test_list_foods(self, client):
        num_of_food = 5
        random_foods = [self._generate_random_food() for _ in range(num_of_food)]
        for food in random_foods:
            await client.post(FOODS_API_ENDPOINT, json=food)

        response = await client.get(FOODS_API_ENDPOINT)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == num_of_food

    async def test_get_food(self, client):
        ham = {
            "name": "ham",
            "quantity": 140,
            "fats": 8,
            "carbs": 2,
            "protein": 29,
        }
        response = await client.post(FOODS_API_ENDPOINT, json=ham)
        assert response.status_code == status.HTTP_201_CREATED
        pk = response.json()["pk"]
        assert pk is not None

        response = await client.get(f"{FOODS_API_ENDPOINT}/{pk}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["pk"] == pk

    def _generate_random_food(self):
        food_item = {
            "name": "".join(random.choices(string.ascii_lowercase, k=5)),
            "quantity": random.randint(1, 100),
            "fats": round(random.uniform(0.1, 50.0), 2),
            "carbs": round(random.uniform(0.0, 100.0), 2),
            "protein": round(random.uniform(0.1, 50.0), 2),
        }
        return food_item


class TestUsersAPI:
    """Test cases for the users API."""

    async def test_create_user(self, client):
        rice_crackers = {
            "name": "rice crackers",
            "quantity": 5,
            "fats": 0,
            "carbs": 15,
            "protein": 1,
        }
        response = await client.post(FOODS_API_ENDPOINT, json=rice_crackers)

        test_user = {
            "name": "Tanjiro",
            "foods": [response.json()["pk"]],
        }
        response = await client.post(USERS_API_ENDPOINT, json=test_user)
        assert response.status_code == status.HTTP_201_CREATED

        pk = response.json().get("pk")
        assert pk is not None

        response = await client.get(USERS_API_ENDPOINT)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json()[0]["pk"] == pk
        assert response.json()[0]["foods"][0]["name"] == "rice crackers"

    async def test_list_users(self, client):
        rice_crackers = {
            "name": "rice crackers",
            "quantity": 5,
            "fats": 0,
            "carbs": 15,
            "protein": 1,
        }
        response = await client.post(FOODS_API_ENDPOINT, json=rice_crackers)
        food_pk = response.json()["pk"]

        for n in range(3):
            await client.post(
                USERS_API_ENDPOINT,
                json={"name": f"test_user_{n}", "foods": [food_pk]},
            )

        response = await client.get(USERS_API_ENDPOINT)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 3

    async def test_get_user(self, client):
        rice_crackers = {
            "name": "rice crackers",
            "quantity": 5,
            "fats": 0,
            "carbs": 15,
            "protein": 1,
        }
        response = await client.post(FOODS_API_ENDPOINT, json=rice_crackers)
        test_user = {
            "name": "Tanjiro Kamado",
            "foods": [response.json()["pk"]],
        }
        response = await client.post(USERS_API_ENDPOINT, json=test_user)
        assert response.status_code == status.HTTP_201_CREATED
        pk = response.json().get("pk")
        assert pk is not None

        response = await client.get(f"{USERS_API_ENDPOINT}/{pk}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["pk"] == pk
