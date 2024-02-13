from django.urls import path
from myapp.consumers import MYCONSUMERS


websocket_urlpatterns=[
    path('chat/<str:group>/ws/sc/',MYCONSUMERS.as_asgi())
]