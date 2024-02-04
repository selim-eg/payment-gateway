from django.urls import path
from .views import OrderCreateAPIView

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateAPIView.as_view(), name='order-create'),
    
]
