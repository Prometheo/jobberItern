from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ConnectionModel, ChatMessage
import json
import boto3


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

def _send_to_connection(connection_id, data):
    gatewayapi=boto3.client('apigatewaymanagementapi',endpoint_url=' https://085rlczqhe.execute-api.us-east-2.amazonaws.com/test/',region_name='us-east-2',aws_access_key_id='AKIAJE7DNVOVQJP7CBRQ',aws_secret_access_key='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')
    return gatewayapi.post_to_connection(ConnectionId=connection_id,Data=json.dumps(data).encode('utf-8'))


def send_message(request):
    body = _parse_body(request.body)
    ChatMessage.objects.create(message=body['message'],username=body['username'],timestamp=body['timestamp'])
    connections = ConnectionModel.objects.all()
    body = [body['message']]
    data = {'message':body}
    for cons in connections:
        _send_to_connection(cons,data)
    return JsonResponse({'message': 'successfully sent'}, status=200)



