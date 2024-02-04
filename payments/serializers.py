from rest_framework import serializers
from .models import Payment,Transaction
from orders.serializers import OrderSerializer



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('payment_token','user') 



class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    payment = PaymentSerializer(read_only=True)
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'


      