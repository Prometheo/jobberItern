from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ConnectionModel, ChatMessage
from django.forms.models import model_to_dict
import json
import boto3



# Create your views here.



def _parse_body(body):
    body_unicode = body.decode('utf-8')
    return json.loads(body_unicode)


@csrf_exempt
def test(request):
    bodi = (request.body).decode('utf-8')
    print(bodi)
    return JsonResponse({'message': 'hello Daud'}, status=200)

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
    gatewayapi=boto3.client('apigatewaymanagementapi',endpoint_url='https://085rlczqhe.execute-api.us-east-2.amazonaws.com/test',
                            region_name='us-east-2',aws_access_key_id='AKIAJE7DNVOVQJP7CBRQ',
                            aws_secret_access_key='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')
    return gatewayapi.post_to_connection(ConnectionId=connection_id,Data=json.dumps(data).encode('utf-8'))

@csrf_exempt
def send_message(request):
    body = _parse_body(request.body)
    newbody = dict(body)
    print(newbody)
    message=newbody['body']["message"]
    username=newbody['body']["username"]
    timestamp=newbody['body']["timestamp"]
    ChatMessage.objects.create(message=message,username=username,timestamp=timestamp)
    messages = {
        "username": username,
        "message": message,
        "timestamp": timestamp
    }
    connections = ConnectionModel.objects.all()
    data = {'messages':[messages]}
    for cons in connections:
        _send_to_connection(cons.connection_id,data)
    return JsonResponse({'message': 'successfully sent'}, status=200)

@csrf_exempt
def get_recent_message(request):
    body = _parse_body(request.body)
    newbody = dict(body)
    connectionId = newbody['connectionId']
    cons = [con.connection_id for con in ConnectionModel.objects.all()]
    connection_id = ConnectionModel.objects.get(connection_id=connectionId)
    chatmodel = ChatMessage.objects.all()
    message_list = []
    data = {'messages': [
        {'message';body['body']['message'] },
        {'username';body['body']['username'] },
        {'timestamp';body['body']['timestamp'] } for con in cons
    ]}



    return JsonResponse(data, status=200)

