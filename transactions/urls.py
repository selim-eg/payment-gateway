from django.urls import path
from .views import show_credit_card_number,create_credit_card_info
app_name = 'transactions'

urlpatterns = [
    path('credit-card/<int:card_id>/', show_credit_card_number, name='show-credit-card'),
    path('credit-card/create/', create_credit_card_info, name='create_credit_card_number'),
]
