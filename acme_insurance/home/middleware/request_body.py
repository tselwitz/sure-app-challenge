import json
from django.http import JsonResponse


class RequestBodyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
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
