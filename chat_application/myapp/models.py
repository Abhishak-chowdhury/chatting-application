from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ChatGroup(models.Model):
    user=models.ForeignKey(User,related_name='chatgroup_user',on_delete=models.CASCADE)
    name=models.CharField(max_length=500)
    password=models.TextField(null=True)
    def  __str__(self):
        return self.name
    
class Chat(models.Model):
    user=models.ForeignKey(User,related_name='chat_user',on_delete=models.CASCADE)
    group=models.ForeignKey(ChatGroup,related_name='chat_group',on_delete=models.CASCADE)
    msg=models.CharField(max_length=500)
    date_time=models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.msg