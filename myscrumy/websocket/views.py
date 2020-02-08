from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ConnectionModel, ChatMessage
import json


# Create your views here.

@csrf_exempt
def test(request):
    return JsonResponse({'message': 'hello Daud'}, status=200)


def _parse_body(body):
    body_unicode = body.decode('utf-8')
    return json.loads(body_unicode)


@csrf_exempt
def connect(request):
    body = _parse_body(request.body)
    ConnectionModel.objects.create(connection_id = body['connectionId'])
    return JsonResponse({'message': 'connect successfully'}, status=200)

@csrf_exempt
def disconnect(request):
    body = _parse_body(request.body)
    trash = body['connectionId']
    ConnectionModel.objects.get(connection_id = trash).delete()
    return JsonResponse({'message': 'disconnect successfully'}, status=200)


