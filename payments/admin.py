from django.contrib import admin
from .models import Customer, Account, PaymentMethod, Payment, Transaction

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'city', 'country')
    search_fields = ('user__username', 'email', 'first_name', 'last_name', 'phone_number')
    list_filter = ('city', 'country')
    date_hierarchy = 'created_at'

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('customer', 'account_number', 'balance', 'currency', 'is_active', 'account_type')
    search_fields = ('customer__user__username', 'account_number')
    list_filter = ('currency', 'is_active', 'account_type')
    date_hierarchy = 'created_at'

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('customer', 'type', 'is_default')
    search_fields = ('customer__user__username', 'type')
    list_filter = ('type', 'is_default')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount_cents', 'currency', 'order', 'payment_token', 'success', 'cancel', 'failure')
    search_fields = ('user__username', 'order__id', 'payment_token')
    list_filter = ('currency',)
    # date_hierarchy = 'order__created_at'

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment', 'order', 'transaction_type', 'amount', 'currency', 'status')
    search_fields = ('user__username', 'payment__payment_token', 'order__id')
    list_filter = ('transaction_type', 'currency', 'status')
    date_hierarchy = 'created_at'

