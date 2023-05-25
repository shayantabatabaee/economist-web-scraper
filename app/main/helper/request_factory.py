import requests
from requests.models import Response


class RequestFactory:

    @staticmethod
    def get(url: str) -> Response:
        return requests.get(url)
