from django.http import JsonResponse, HttpResponse
from django.views import View
from uuid import UUID


class API_CRUD(View):
    def __init__(self, baseClass, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.baseClass = baseClass

    def get(self, request):
        try:
            params = {i: request.GET.get(f"{i}", "") for i in request.GET}
        except AttributeError:
            return JsonResponse({"error": "Invalid query params"}, status=400)
        obj = self.baseClass.objects.filter(**params).all()
        return JsonResponse([o.pretty_print() for o in obj], safe=False)

    def post(self, request):
        try:
            params = {i: request.body_json[i] for i in request.body_json}
        except AttributeError:
            return JsonResponse({"error": "Invalid JSON request body"}, status=400)

        obj, created = self.baseClass.objects.update_or_create(
            id=params["id"], defaults=params
        )

        try:
            return JsonResponse(obj.pretty_print(), safe=False)
        except AttributeError:
            return JsonResponse(
                {"error": "Object does not have a pretty_print() method"}, status=400
            )

    def delete(self, request):
        try:
            obj_id = UUID(request.body_json["id"])
        except (AttributeError, KeyError):
            return JsonResponse({"error": "Invalid JSON request body"}, status=400)
        except TypeError:
            return JsonResponse({"error": "Invalid UUID format"}, status=400)
        self.baseClass.objects.filter(id=obj_id).delete()
        return HttpResponse(f"Deleted {obj_id}")
