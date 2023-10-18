import json
from uuid import UUID
from django.http import JsonResponse
from decimal import Decimal


class RequestBodyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method != "GET":
            body_unicode = request.body.decode("utf-8")

            if body_unicode:
                try:
                    setattr(request, "body_json", json.loads(body_unicode))
                except json.JSONDecodeError:
                    return JsonResponse(
                        {"error": "Invalid JSON provided in request body."}, status=400
                    )
            else:
                setattr(request, "body_json", {})

            response = self.get_response(request)
            return response
        else:
            return self.get_response(request)


class ConvertNumbersToDecimal:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method != "GET":
            for i in request.body_json:
                if type(request.body_json[i]) in (float, int):
                    request.body_json[i] = Decimal(request.body_json[i])
            response = self.get_response(request)
            return response
        else:
            return self.get_response(request)
