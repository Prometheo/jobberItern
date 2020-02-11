from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ConnectionModel, ChatMessage
from django.forms.models import model_to_dict
import json, os
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
                            region_name='us-east-2',aws_access_key_id= os.environ.get('AWS_ACCESS_KEY'),
                            aws_secret_access_key= os.environ.get('AWS_SECRET_KEY'))
    return gatewayapi.post_to_connection(ConnectionId=connection_id,Data=json.dumps(data).encode('utf-8'))

@csrf_exempt
def send_message(request):
    body = _parse_body(request.body)
    newbody = dict(body)
    con_key = newbody['connectionId']
    connection_id = ConnectionModel.objects.get(connection_id = con_key)
    message=newbody['body']["message"]
    username=newbody['body']["username"]
    timestamp=newbody['body']["timestamp"]
    ChatMessage.objects.create(message=message,username=username,timestamp=timestamp, con_id = connection_id)
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
    #body = _parse_body(request.body)
    #connectionId = body['connectionId']
    chats = ChatMessage.objects.all()
    cons = [con.connection_id for con in ConnectionModel.objects.all()]
    #connection_id = ConnectionModel.objects.get(connection_id=connectionId)
    message_list = []
    for message in chats:
        if message.con_id.connection_id in cons:
            message_list.append(model_to_dict(message))

    for itr in message_list:
        del(itr['id'])
        del(itr['con_id'])

    message_list.reverse()

    recent_messages = {'messages':message_list}

    for konet in cons:
        _send_to_connection(konet, recent_messages)
    
    return JsonResponse(recent_messages, status=200)

