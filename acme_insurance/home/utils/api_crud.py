from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
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
            return HttpResponseBadRequest("Invalid query params")
        obj = self.baseClass.objects.filter(**params).values()
        return JsonResponse(list(obj), safe=False)

    def post(self, request):
        try:
            params = {i: request.body_json[i] for i in request.body_json}
        except AttributeError:
            return HttpResponseBadRequest("Invalid JSON request body")

        obj, created = self.baseClass.objects.update_or_create(
            id=params["id"], defaults=params
        )

        try:
            return JsonResponse(obj.pretty_print(), safe=False)
        except AttributeError:
            return HttpResponseBadRequest(
                "Object does not have a pretty_print() method"
            )

    def delete(self, request):
        try:
            obj_id = UUID(request.body_json["id"])
        except (AttributeError, KeyError):
            return HttpResponseBadRequest("Invalid JSON request body")
        except TypeError:
            return HttpResponseBadRequest("Invalid UUID format")
        self.baseClass.objects.filter(id=obj_id).delete()
        return HttpResponse(f"Deleted {obj_id}")
