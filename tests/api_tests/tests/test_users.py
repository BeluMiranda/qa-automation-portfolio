"""
Tests: Users API — JSONPlaceholder & DummyJSON
Covers: GET users, POST user, PUT/PATCH, DELETE, pagination, schema validation.

Target APIs:
  - https://jsonplaceholder.typicode.com/users  (10 users, simple fake API)
  - https://dummyjson.com/users                 (30 users, richer fake API)
"""
import json
import pytest
import allure
from pathlib import Path

from tests.api_tests.helpers.api_client import APIClient

PAYLOADS = json.loads(
    (Path(__file__).parent.parent / "fixtures" / "payloads.json").read_text()
)

# Required keys in a DummyJSON user object
DUMMYJSON_USER_SCHEMA = {"id", "firstName", "lastName", "email", "phone", "username"}


@allure.feature("Users API")
@allure.story("User Management")
class TestUsersAPI:
    """
    Users API test suite — JSONPlaceholder + DummyJSON.
    No authentication required. All public endpoints.
    """

    # ------------------------------------------------------------------
    # JSONPlaceholder — /users
    # ------------------------------------------------------------------

    @allure.title("TC_API_USR_001 - GET /users returns 10 users")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_all_users_returns_10(self, jsonplaceholder_client: APIClient):
        """JSONPlaceholder /users returns exactly 10 users with status 200."""
        response = jsonplaceholder_client.get("/users")

        jsonplaceholder_client.assert_status(response, 200)
        users = response.json()
        assert isinstance(users, list)
        assert len(users) == 10

    @allure.title("TC_API_USR_002 - GET /users/{id} returns correct user schema")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_user_by_id(self, jsonplaceholder_client: APIClient):
        """GET /users/1 returns the user with correct ID and required fields."""
        response = jsonplaceholder_client.get("/users/1")

        jsonplaceholder_client.assert_status(response, 200)
        jsonplaceholder_client.assert_json_value(response, "id", 1)

        user = response.json()
        for key in {"id", "name", "username", "email", "phone", "website"}:
            assert key in user, f"Missing required field: '{key}'"

    @allure.title("TC_API_USR_003 - GET /users/{id} 404 for non-existent user")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_get_nonexistent_user_returns_404(self, jsonplaceholder_client: APIClient):
        """GET /users/9999 should return 404."""
        response = jsonplaceholder_client.get("/users/9999")
        jsonplaceholder_client.assert_status(response, 404)

    @allure.title("TC_API_USR_004 - GET /users?id=1 filters correctly")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.api
    def test_filter_users_by_id(self, jsonplaceholder_client: APIClient):
        """GET /users?id=1 returns only the user with id=1."""
        response = jsonplaceholder_client.get("/users", params={"id": 1})

        jsonplaceholder_client.assert_status(response, 200)
        users = response.json()
        assert len(users) == 1
        assert users[0]["id"] == 1

    # ------------------------------------------------------------------
    # DummyJSON — /users
    # ------------------------------------------------------------------

    @allure.title("TC_API_USR_005 - DummyJSON GET /users returns paginated list")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_dummyjson_get_users_list(self, dummyjson_client: APIClient):
        """DummyJSON /users returns paginated response with correct envelope schema."""
        response = dummyjson_client.get("/users")

        dummyjson_client.assert_status(response, 200)
        body = response.json()

        for key in ("users", "total", "skip", "limit"):
            assert key in body, f"Missing envelope key: '{key}'"

        for user in body["users"]:
            missing = DUMMYJSON_USER_SCHEMA - user.keys()
            assert not missing, f"User missing fields: {missing}"

    @allure.title("TC_API_USR_006 - DummyJSON GET /users/{id} returns single user")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_dummyjson_get_single_user(self, dummyjson_client: APIClient):
        """DummyJSON /users/1 returns user with id=1 and valid schema."""
        response = dummyjson_client.get("/users/1")

        dummyjson_client.assert_status(response, 200)
        dummyjson_client.assert_json_value(response, "id", 1)

        user = response.json()
        for key in DUMMYJSON_USER_SCHEMA:
            assert key in user, f"Missing field: '{key}'"

    @allure.title("TC_API_USR_007 - DummyJSON GET /users/{id} 404 for unknown user")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_dummyjson_user_not_found(self, dummyjson_client: APIClient):
        """DummyJSON returns 404 for a user ID that does not exist."""
        response = dummyjson_client.get("/users/9999")
        dummyjson_client.assert_status(response, 404)

    @allure.title("TC_API_USR_008 - DummyJSON POST /users/add creates a user")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_dummyjson_create_user(self, dummyjson_client: APIClient):
        """POST /users/add returns 201 with the new user including generated ID."""
        payload = {
            "firstName": "QA",
            "lastName": "Engineer",
            "email": "qa.engineer@portfolio.dev",
            "username": "qaengineer_portfolio",
        }
        response = dummyjson_client.post("/users/add", json=payload)

        dummyjson_client.assert_status(response, 201)
        body = response.json()

        assert body["firstName"] == payload["firstName"]
        assert body["lastName"] == payload["lastName"]
        assert "id" in body

    @allure.title("TC_API_USR_009 - DummyJSON PUT /users/{id} fully updates a user")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_dummyjson_put_user(self, dummyjson_client: APIClient):
        """PUT /users/1 replaces user data and returns the updated resource."""
        payload = {"lastName": "UpdatedLastName"}
        response = dummyjson_client.put("/users/1", json=payload)

        dummyjson_client.assert_status(response, 200)
        dummyjson_client.assert_json_value(response, "lastName", "UpdatedLastName")

    @allure.title("TC_API_USR_010 - DummyJSON pagination: limit & skip work correctly")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.api
    def test_dummyjson_pagination(self, dummyjson_client: APIClient):
        """GET /users?limit=5&skip=0 and skip=5 return different users."""
        page1 = dummyjson_client.get("/users", params={"limit": 5, "skip": 0}).json()["users"]
        page2 = dummyjson_client.get("/users", params={"limit": 5, "skip": 5}).json()["users"]

        ids_page1 = {u["id"] for u in page1}
        ids_page2 = {u["id"] for u in page2}

        assert len(ids_page1) == 5
        assert len(ids_page2) == 5
        assert ids_page1.isdisjoint(ids_page2), f"Pages share users: {ids_page1 & ids_page2}"
