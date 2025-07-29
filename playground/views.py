from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.views import APIView
import requests
import logging

logger = logging.getLogger(__name__)


class HelloView(APIView):

    # @method_decorator(cache_page(5 * 60))
    def get(self, request: HttpRequest):

        try:
            logger.info("Calling httpbin")
            requests.get("https://httpbin.org/delay/2")
            logger.info("Received the response")

        except requests.exceptions.ConnectionError:
            logger.critical("Connection to httpbin failed")

        return render(request, "hello.html", {"name": "King"})
