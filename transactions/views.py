from django.shortcuts import render
from django.http import HttpResponse
from .models import CreditCard
# from cryptography.fernet import Fernet


# fernet_key = "2qqu0TnzDNI4riD52dREVdXLSzDSpLQ0czGs2GY-sLQ="

# cipher_suite = Fernet(fernet_key)

def show_credit_card_number(request, card_id):
    try:
        credit_card = CreditCard.objects.get(id=card_id)
        decrypted_card_number = credit_card.get_card_number() 
        return HttpResponse(f"Card Number: {decrypted_card_number}")
    except CreditCard.DoesNotExist:
        return HttpResponse("Credit Card not found.", status=404)


def create_credit_card_info(request):
    try:
        
        credit_card = CreditCard(
            card_number = "1234123412341234",
            card_expiry='2024-12-31',
            cardholder_name='John Doe',
            card_cvv = "234",
            user=request.user
        )

        credit_card.save()

        
        retrieved_card = CreditCard.objects.get(id=credit_card.id)
        print(retrieved_card.get_card_info())  
        return HttpResponse(f"Card Info: {retrieved_card.get_card_info()}")
    
    except CreditCard.DoesNotExist:
        return HttpResponse("Credit Card not found.", status=404)