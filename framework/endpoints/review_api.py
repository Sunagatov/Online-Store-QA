import json
from typing import Dict, Any

import requests
from requests import Response

from configs import HOST
from framework.asserts.common import assert_status_code
from framework.tools.logging_allure import log_request


class ReviewAPI:
    def __init__(self):
        self.url = f"{HOST}/api/v1/products"
        self.headers = {"Content-Type": "application/json"}

    def get_all_product_reviews(
        self, product_id: str, expected_status_code: int = 200, **filters
    ) -> Response:
        """Getting info about user via API

        Args:
            product_id: id of product
            expected_status_code: Expected HTTP code from Response

        """
        headers = self.headers
        url = f"{self.url}/{product_id}/reviews"
        response = requests.get(url, headers=headers, params=filters)
        print(url)
        assert_status_code(response, expected_status_code=expected_status_code)
        log_request(response)

        return response

    def delete_product_review(
        self,
        token: str,
        product_id: str,
        review_id: str,
        expected_status_code: int = 200,
    ) -> Response:
        """Deleting user

        Args:
            review_id: id of review
            product_id: id of product
            expected_status_code: Expected HTTP code from Response
            token: JWT token for authorization of request

        """
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        url = f"{self.url}/{product_id}/reviews/{review_id}"
        response = requests.delete(headers=headers, url=url)
        assert_status_code(response, expected_status_code=expected_status_code)
        log_request(response)
        return response

    def add_product_review(
        self,
        token: str,
        product_id: str,
        text_review: str,
        rating: int,
        expected_status_code: int = 200,
    ) -> Response:
        """Deleting user

        Args:
            rating: rate of product
            text_review: text for product review
            product_id: product id for review
            expected_status_code: Expected HTTP code from Response
            token: JWT token for authorization of request

        """
        data = {"text": text_review, "rating": rating}
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        url = f"{self.url}/{product_id}/reviews"
        response = requests.post(headers=headers, url=url, data=json.dumps(data))
        assert_status_code(response, expected_status_code=expected_status_code)
        log_request(response)
        return response

    def get_user_product_review(
        self, product_id: str, token: str, expected_status_code: int = 200
    ) -> Response:
        """Getting info about user via API

        Args:
            token: JWT token for authorization of request
            product_id: ID of product
            expected_status_code: Expected HTTP code from Response

        """
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        url = f"{self.url}/{product_id}/review"
        response = requests.get(headers=headers, url=url)
        assert_status_code(response, expected_status_code=expected_status_code)
        log_request(response)

        return response

    def like_dislike_product_review(
        self,
        product_id: str,
        token: str,
        product_review_id: str,
        expected_status_code: int = 200,
        is_like: bool = True,
    ) -> Response:
        """Getting info about user via API

        Args:
            is_like: like or dislike(True or False)
            product_review_id: ID of product review
            token: JWT token for authorization of request
            product_id: ID of product
            expected_status_code: Expected HTTP code from Response

        """
        headers = self.headers
        data = {"isLike": is_like}
        headers["Authorization"] = f"Bearer {token}"
        url = f"{self.url}/{product_id}/reviews/{product_review_id}/rate"
        response = requests.post(headers=headers, data=json.dumps(data), url=url)
        assert_status_code(response, expected_status_code=expected_status_code)
        log_request(response)

        return response

    def get_product_review_statistics(self, product_id: str) -> Response:
        """Getting product review statistics

        Args:
            product_id: ID of product
        """
        url = f"{self.url}/{product_id}/reviews/statistics"
        response = requests.get(url=url)
        log_request(response)

        return response
