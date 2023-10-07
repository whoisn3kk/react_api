from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from .models import *
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

@csrf_exempt
def products(request):
    products = Products.objects.all()
    res = []
    for p in products:
        dictor = {}
        dictor["uuid"] = p.uuid
        dictor["title"] = p.title
        dictor["price"] = p.price
        dictor["imageUrl"] = p.imageUrl
        res.append(dictor)
    print(res)
    return JsonResponse(res, safe=False)


@csrf_exempt
def cart(request, path):
    info = path.split('/')
    Model = apps.get_model("myapp", info[0].capitalize())
    print(Model.objects.all())
    if request.method == "GET":
        products = Model.objects.all()
        res = []
        for p in products:
            dictor = {}
            dictor["uuid"] = p.uuid
            dictor["title"] = p.title
            dictor["price"] = p.price
            dictor["imageUrl"] = p.imageUrl
            res.append(dictor)
        print(res)
        return JsonResponse(res, safe=False)
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        p_id = data[0]["uuid"]
        p = Products.objects.get(uuid=p_id)
        c = Model.objects.create(product_link=p)
        c.save()
        return HttpResponse("ok")
    if request.method == "DELETE":
        p_uuid = info[1]
        p = Products.objects.get(uuid=p_uuid)
        Model.objects.filter(product_link=p).first().delete()
        return HttpResponse('ok')
    return HttpResponse('bad')
    

@csrf_exempt
def cart_del(request, path, p_uuid):
    print(f"path:{path}, uuid:{p_uuid}")
    if request.method == "DELETE":
        p = Products.objects.get(uuid=p_uuid)
        Cart.objects.filter(product_link=p).first().delete()
        return HttpResponse('ok')
    return HttpResponse('bad')
    

@csrf_exempt
def likes(request):
    ...