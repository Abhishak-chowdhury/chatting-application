from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer
from myapp.models import *
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
import json
import datetime

class MYCONSUMERS(SyncConsumer):
    def websocket_connect(self, event):
        print("websocket conected......",event)
        print("websocket conected......",self.channel_name)
        self.groupname=self.scope['url_route']['kwargs']['group']
        async_to_sync(self.channel_layer.group_add)(self.groupname,self.channel_name)
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        print("message are received.....",event)
        data=json.loads(event["text"])
        data["user"]=self.scope["user"].username
        user_obj=User.objects.get(username=self.scope["user"].username)
        group_obj=ChatGroup.objects.get(name=self.groupname)
        Chat.objects.create(user=user_obj,group=group_obj,msg=data["message"])
        # date=Chat.objects.get(user=user_obj,group=group_obj,msg=data["message"]).date_time
        # data["date"]=date
        # now = datetime.datetime.now()
        # data["date"]=now
        async_to_sync(self.channel_layer.group_send)(self.groupname,{
                "type": "chat.message",
                "message": json.dumps(data),
            })
    def chat_message(self, event):
        self.send({
            "type": "websocket.send",
            "text": event["message"],
        })
        
    def websocket_disconnect(self, event):
        print("disconnected.....",event)
        async_to_sync(self.channel_layer.group_discard)(self.groupname,self.channel_name)
        raise StopConsumer()  

    
