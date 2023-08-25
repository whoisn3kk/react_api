from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from myapp.models import Api
import json

@csrf_exempt
def main(request):
    if request.method == "POST":
        json_data = request.body.decode('utf-8')
        a = Api(json=json_data)
        a.save()
        return JsonResponse({"uuid": str(a.uuid)})
    return HttpResponse("""<form method="POST"><textarea name="json"></textarea><br><button type="submit">Save</button></form>""")

@csrf_exempt
def api(request):
    if request.method == "GET":
        uuid = request.GET.get("uuid")
        try:
            a = Api.objects.get(uuid=uuid)
            return HttpResponse(a.json, content_type='application/json')
        except Api.DoesNotExist:
            return JsonResponse({"error": "API data not found"}, status=404)
    
    elif request.method == "DELETE":
        uuid = request.GET.get("uuid")
        try:
            a = Api.objects.get(uuid=uuid)
            a.delete()
            return JsonResponse({"message": "API data deleted"})
        except Api.DoesNotExist:
            return JsonResponse({"error": "API data not found"}, status=404)
    
    elif request.method == "POST":
        uuid = request.GET.get("uuid")
        json_data = request.body.decode("utf-8")  # Assuming you are sending the JSON data in the "json" field	
        try:
            json_dict = json.loads(json_data)
            if uuid:
                try:
                    a = Api.objects.get(uuid=uuid)
                    a.json = json_data
                    a.save()	
                    return JsonResponse({"message": "API data updated", "uuid": str(a.uuid)})
                except Api.DoesNotExist:
                    return JsonResponse({"error": "API data not found"}, status=404)
            else:
                return JsonResponse({"error": "No UUID provided in URL"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    
    return JsonResponse({"error": "Invalid method"}, status=405)