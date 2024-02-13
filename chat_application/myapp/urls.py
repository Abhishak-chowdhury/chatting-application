from django.urls import path
from myapp.views import *
urlpatterns = [
 
    path('',SignUp,name='signup'),
    path('signin/',SignIn,name='signin'),
    path('logout',Logout,name='logout'),
    path('join/room',Join_Room,name='joinroom'),
    path('create/room',Create_Room,name='createroom'),
    path('roomvalidate',Room_validity,name='roomvalidate'),
    path('chat/<str:room_name>',Chatting,name='chat'),
]