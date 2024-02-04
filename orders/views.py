from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated

class OrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # POST /orders/create/
    @swagger_auto_schema(
        operation_id="Create a new order",
        tags=["Checkout Flow"],  
        operation_description="""
            post:
            Create a new order with items and shipping details.

            Payload example:
            {
                
                "delivery_needed": "false",
                "amount_cents": "100",
                "currency": "EGP",
                "merchant_order_id": 5,
                "items": [
                    {
                        "name": "ASC1515",
                        "amount_cents": "500000",
                        "description": "Smart Watch",
                        "quantity": "1"
                    },
                    {
                        "name": "ERT6565",
                        "amount_cents": "200000",
                        "description": "Power Bank",
                        "quantity": "1"
                    }
                ],
                "shipping_data": {
                    "apartment": "803",
                    "email": "claudette09@exa.com",
                    "floor": "42",
                    "first_name": "Clifford",
                    "street": "Ethan Land",
                    "building": "8028",
                    "phone_number": "+86(8)9135210487",
                    "postal_code": "01898",
                    "extra_description": "8 Ram , 128 Giga",
                    "city": "Jaskolskiburgh",
                    "country": "CR",
                    "last_name": "Nicolas",
                    "state": "Utah"
                },
                "shipping_details": {
                    "notes": "test",
                    "number_of_packages": 1,
                    "weight": 1,
                    "weight_unit": "Kilogram",
                    "length": 1,
                    "width": 1,
                    "height": 1,
                    "contents": "product of some sorts"
                }
            }
        """,
        request_body=OrderSerializer,
        responses={
            201: openapi.Response(
                description="Order created successfully",
                examples={
                    "application/json": {
                        
                        "delivery_needed": "boolean",
                        "amount_cents": "integer",
                        "currency": "string",
                        "merchant_order_id": "integer",
                        "items": [
                            {
                                "name": "string",
                                "amount_cents": "integer",
                                "description": "string",
                                "quantity": "integer"
                            }
                        ],
                        "shipping_data": {
                            "apartment": "string",
                            "email": "string",
                            "floor": "string",
                            "first_name": "string",
                            "street": "string",
                            "building": "string",
                            "phone_number": "string",
                            "postal_code": "string",
                            "extra_description": "string",
                            "city": "string",
                            "country": "string",
                            "last_name": "string",
                            "state": "string"
                        },
                        "shipping_details": {
                            "notes": "string",
                            "number_of_packages": "integer",
                            "weight": "number",
                            "weight_unit": "string",
                            "length": "number",
                            "width": "number",
                            "height": "number",
                            "contents": "string"
                        }
                    }
                }
            ),
            400: "Bad Request"
        }
    )
    def post(self, request, *args, **kwargs):
        # serializer = OrderSerializer(data=request.data)
        serializer = OrderSerializer(
            data=request.data, 
            context={'request': request}
            )
        if serializer.is_valid():
            serializer.save(user=request.user)  
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


