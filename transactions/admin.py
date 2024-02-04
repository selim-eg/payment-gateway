from django.contrib import admin
from .models import Account,CreditCard,Transaction
# Register your models here.
admin.site.register(Account)
admin.site.register(Transaction)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = [ 'get_card_number_last_digits']
    readonly_fields = ['card_number', 'card_expiry', 'cardholder_name', 'card_cvv']

    def get_card_number_last_digits(self, obj):
        return obj.get_card_info()
    get_card_number_last_digits.short_description = 'Card info'

    def has_delete_permission(self, request, obj=None):
        return False
        
    def has_change_permission(self, request, obj=None):
        return False
admin.site.register(CreditCard, CreditCardAdmin)