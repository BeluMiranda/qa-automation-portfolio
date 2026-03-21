"""
Tests: Posts API — JSONPlaceholder
Covers: GET list, GET single, POST, PUT, PATCH, DELETE.
Target: https://jsonplaceholder.typicode.com/posts
"""
import json
import pytest
import allure
from pathlib import Path

from tests.api_tests.helpers.api_client import APIClient

PAYLOADS = json.loads(
    (Path(__file__).parent.parent / "fixtures" / "payloads.json").read_text()
)


@allure.feature("Posts API")
@allure.story("CRUD Operations")
class TestPostsAPI:
    """
    REST API test suite for /posts endpoint.
    Uses JSONPlaceholder — a public fake REST API for testing.
    """

    # ------------------------------------------------------------------
    # GET
    # ------------------------------------------------------------------

    @allure.title("TC_API_POST_001 - GET /posts returns list of 100")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_all_posts_returns_100(self, jsonplaceholder_client: APIClient):
        """GET /posts should return 100 posts with status 200."""
        response = jsonplaceholder_client.get("/posts")

        jsonplaceholder_client.assert_status(response, 200)
        posts = response.json()
        assert isinstance(posts, list)
        assert len(posts) == 100

    @allure.title("TC_API_POST_002 - GET /posts/{id} returns correct post")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_post_by_id(self, jsonplaceholder_client: APIClient):
        """GET /posts/1 returns the post with id=1."""
        response = jsonplaceholder_client.get("/posts/1")

        jsonplaceholder_client.assert_status(response, 200)
        jsonplaceholder_client.assert_json_value(response, "id", 1)
        jsonplaceholder_client.assert_json_key(response, "title")
        jsonplaceholder_client.assert_json_key(response, "body")
        jsonplaceholder_client.assert_json_key(response, "userId")

    @allure.title("TC_API_POST_003 - GET /posts/{id} 404 for non-existent post")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_get_non_existent_post_returns_404(self, jsonplaceholder_client: APIClient):
        """GET /posts/9999 should return 404."""
        response = jsonplaceholder_client.get("/posts/9999")
        jsonplaceholder_client.assert_status(response, 404)

    @allure.title("TC_API_POST_004 - GET /posts?userId=1 filters by user")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_get_posts_filtered_by_user(self, jsonplaceholder_client: APIClient):
        """GET /posts?userId=1 returns only posts belonging to user 1."""
        response = jsonplaceholder_client.get("/posts", params={"userId": 1})

        jsonplaceholder_client.assert_status(response, 200)
        posts = response.json()
        assert all(post["userId"] == 1 for post in posts), (
            "Not all posts belong to userId=1"
        )

    @allure.title("TC_API_POST_005 - GET /posts response time under 2 seconds")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.api
    def test_get_posts_response_time(self, jsonplaceholder_client: APIClient):
        """GET /posts should respond within 2000ms."""
        response = jsonplaceholder_client.get("/posts")
        jsonplaceholder_client.assert_response_time(response, max_ms=2000)

    # ------------------------------------------------------------------
    # POST
    # ------------------------------------------------------------------

    @allure.title("TC_API_POST_006 - POST /posts creates a new post")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_create_post_returns_201(self, jsonplaceholder_client: APIClient):
        """POST /posts with valid body returns 201 and the created resource."""
        payload = PAYLOADS["create_post"]["valid"]
        response = jsonplaceholder_client.post("/posts", json=payload)

        jsonplaceholder_client.assert_status(response, 201)
        body = response.json()
        assert body["title"] == payload["title"]
        assert body["body"] == payload["body"]
        assert body["userId"] == payload["userId"]
        assert "id" in body

    # ------------------------------------------------------------------
    # PUT
    # ------------------------------------------------------------------

    @allure.title("TC_API_POST_007 - PUT /posts/{id} fully updates a post")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_put_post_returns_200(self, jsonplaceholder_client: APIClient):
        """PUT /posts/1 replaces the resource and returns 200."""
        payload = PAYLOADS["update_post"]["full"]
        response = jsonplaceholder_client.put("/posts/1", json=payload)

        jsonplaceholder_client.assert_status(response, 200)
        jsonplaceholder_client.assert_json_value(response, "title", payload["title"])

    # ------------------------------------------------------------------
    # PATCH
    # ------------------------------------------------------------------

    @allure.title("TC_API_POST_008 - PATCH /posts/{id} partially updates a post")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_patch_post_returns_200(self, jsonplaceholder_client: APIClient):
        """PATCH /posts/1 updates only the provided fields."""
        payload = PAYLOADS["update_post"]["partial"]
        response = jsonplaceholder_client.patch("/posts/1", json=payload)

        jsonplaceholder_client.assert_status(response, 200)
        jsonplaceholder_client.assert_json_value(response, "title", payload["title"])

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    @allure.title("TC_API_POST_009 - DELETE /posts/{id} returns 200")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_delete_post_returns_200(self, jsonplaceholder_client: APIClient):
        """DELETE /posts/1 removes the resource and returns 200."""
        response = jsonplaceholder_client.delete("/posts/1")
        jsonplaceholder_client.assert_status(response, 200)

    @allure.title("TC_API_POST_010 - GET /posts/{id}/comments returns comments")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.api
    def test_get_post_comments(self, jsonplaceholder_client: APIClient):
        """GET /posts/1/comments returns a list of comments for the post."""
        response = jsonplaceholder_client.get("/posts/1/comments")

        jsonplaceholder_client.assert_status(response, 200)
        comments = response.json()
        assert isinstance(comments, list)
        assert len(comments) > 0
        assert all(c["postId"] == 1 for c in comments)
