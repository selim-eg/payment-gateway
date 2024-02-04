from django.db import models
# from django.utils.translation import gettext_lazy as _
class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    # auth_token = models.CharField(max_length=255)
    delivery_needed = models.BooleanField(default=False)
    amount_cents = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=("amount cents"))
    currency = models.CharField(max_length=3)
    merchant_order_id = models.IntegerField(unique=True)



class Item(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount_cents = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=("amount cents"))
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()

class ShippingData(models.Model):
    order = models.OneToOneField(Order, related_name='shipping_data', on_delete=models.CASCADE)
    apartment = models.CharField(max_length=255)
    email = models.EmailField()
    floor = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    building = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    extra_description = models.TextField()
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

class ShippingDetails(models.Model):
    order = models.OneToOneField(Order, related_name='shipping_details', on_delete=models.CASCADE)
    notes = models.TextField()
    number_of_packages = models.IntegerField()
    weight = models.FloatField()
    weight_unit = models.CharField(max_length=255)
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    contents = models.TextField()



class TestCard(models.Model):
    card_number = models.CharField(max_length=500)  
    card_expiry = models.CharField(max_length=500)
    cardholder_name = models.CharField(max_length=500)
    card_cvv = models.CharField(max_length=500)
    status =  models.CharField(max_length=50, choices=[('success', 'success'), ('cancel', 'cancel'), ('failure', 'failure')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.cardholder_name}"