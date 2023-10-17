from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views import View
from uuid import UUID
from django.http import HttpResponse


class API_CRUD(View):
    def __init__(self, baseClass, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.baseClass = baseClass

    def get(self, request):
        params = {i: request.body_json[i] for i in request.body_json}
        obj = self.baseClass.objects.filter(**params).values()
        return JsonResponse(list(obj), safe=False)

    def post(self, request):
        params = {i: request.body_json[i] for i in request.body_json}
        obj, created = self.baseClass.objects.update_or_create(**params)
        return JsonResponse(obj.get_dict(), safe=False)

    def delete(self, request):
        print(request.body_json["id"])
        obj = self.baseClass.objects.filter(id=UUID(request.body_json["id"])).delete()
        return HttpResponse(f"Deleted {request.body_json['id']}")
