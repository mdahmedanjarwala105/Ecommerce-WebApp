from django.shortcuts import render
from django.http import HttpRequest
import requests
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from django.utils.decorators import method_decorator


class HelloView(APIView):

    @method_decorator(cache_page(5 * 60))
    def get(self, request: HttpRequest):

        requests.get("https://httpbin.org/delay/2")

        return render(request, "hello.html", {"name": "King"})
