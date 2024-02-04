from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.db import transaction
from django.views import View

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Payment,Transaction
from .serializers import PaymentSerializer,TransactionSerializer
from rest_framework import generics

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from orders.models import TestCard

class PaymentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=PaymentSerializer,
        operation_id="Create a new payment",
        tags=["Checkout Flow"],
        operation_description="""
            post:
            Create a new payment for an order.

            Payload example:
            {
               
                "amount_cents": 10000,
                "expiration": 3600,
                "order": 1,
                "billing_data": {
                                "apartment": "803", 
                                "email": "claudette09@exa.com", 
                                "floor": "42", 
                                "first_name": "Clifford", 
                                "street": "Ethan Land", 
                                "building": "8028", 
                                "phone_number": "+86(8)9135210487", 
                                "shipping_method": "PKG", 
                                "postal_code": "01898", 
                                "city": "Jaskolskiburgh", 
                                "country": "CR", 
                                "last_name": "Nicolas", 
                                "state": "Utah"
                            }, 
                "currency": "EGP",
                "integration_id": 1,
                "lock_order_when_paid": false,
                "success": "https://your-store/success",
                "cancel": "https://your-store/cancel",
                "failure": "https://your-store/failure"
            }
        """, 
        responses={
            201: openapi.Response(
                description="Payment created successfully",
                examples={
                    "application/json": {
                        "token":"fed09bfa-594e-4f31-9585-3a471a52fed0"
                        # "user": "user_id",
                        # "amount_cents": 1000,
                        # "expiration": 3600,
                        # "order": "order_id",
                        # "billing_data": {
                        #     "credit_card_number": "xxxx-xxxx-xxxx-xxxx",
                        #     "expiration_date": "MM/YY"
                        # },
                        # "currency": "USD",
                        # "integration_id": 1,
                        # "lock_order_when_paid": False
                    }
                }
            ),
            400: "Bad Request"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            payment = serializer.save(user=request.user)
            return Response({
                'token': str(payment.payment_token),
                "url":request.build_absolute_uri(
                        reverse('payments:checkout-page', args=[str(payment.payment_token)] )
                      )
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CheckoutPageView(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        payment = get_object_or_404(Payment, payment_token=kwargs['token'])
        context = {"payment": payment}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        payment = get_object_or_404(Payment, payment_token=kwargs['token'])
        cardholder_name = request.POST.get("cardholder_name")
        card_number = request.POST.get("card_number")
        card_cvv = request.POST.get("card_cvv")

        try:
            test_card = TestCard.objects.get(
                cardholder_name=cardholder_name,
                card_number=card_number,
                card_cvv=card_cvv
            )
        except TestCard.DoesNotExist:
            raise Http404("Test card not found.")

        status_mapping = {
            "success": ("paid", payment.success),
            "cancel": ("cancelled", payment.cancel),
            "failure": ("failed", payment.failure)
        }

        transaction_status, redirect_url = status_mapping.get(test_card.status, (None, None))

        if transaction_status:
            transaction_id = None
            with transaction.atomic():
                transaction_id = Transaction.objects.create(
                    user=payment.user,
                    payment=payment,
                    order=payment.order,
                    amount=payment.amount_cents,
                    currency=payment.currency,
                    status=transaction_status,
                    transaction_type="charge"
                )

            redirect_path = f"{redirect_url}&transaction_id={transaction_id.id}"
            return redirect(redirect_path)

        
        context = {"payment": payment, "error": "Invalid card status."}
        return render(request, self.template_name, context)
    


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user)
    

class TransactionDetailAPIView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer    
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        
        return Transaction.objects.filter(user=self.request.user)
    



class TransactionViewSet(viewsets.ViewSet):

    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        user = self.request.user
        return Transaction.objects.filter(user=user)

    # def list(self, request):

    #     queryset = self.get_queryset()
    #     serializer = self.serializer_class(queryset, many=True)
    #     return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='refund')
    def set_refund(self, request, pk=None):

        transaction = self.get_object_or_404(pk)

       
        if transaction.user != request.user:
            raise PermissionDenied("You do not have permission to perform this action.")

       
        if transaction.status == 'refund':
            return Response({"detail": "Transaction is already set to refund."},
                            status=status.HTTP_409_CONFLICT)

       
        transaction.status = 'refund'
        transaction.save(update_fields=['status'])
        return Response({"detail": "Transaction status updated to refund."},
                        status=status.HTTP_200_OK)

    def get_object_or_404(self, pk):

        try:
            return self.get_queryset().get(pk=pk)
        except Transaction.DoesNotExist:
            raise NotFound("A transaction with this ID does not exist.")    