from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (PaymentCreateAPIView,CheckoutPageView,
                    TransactionDetailAPIView,TransactionListView,
                    TransactionViewSet)

app_name = "payments"

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')


urlpatterns = [
    path('', include(router.urls)),
    path('create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('checkout/<uuid:token>',CheckoutPageView.as_view() , name="checkout-page"),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', TransactionDetailAPIView.as_view(), name='transaction-detail'),
    
]
