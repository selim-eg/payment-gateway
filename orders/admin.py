from django.contrib import admin
from .models import Order, Item, ShippingData, ShippingDetails, TestCard

class ItemInline(admin.TabularInline):
    model = Item
    extra = 1
    fields = ('name', 'amount_cents', 'description', 'quantity')

class ShippingDataInline(admin.StackedInline):
    model = ShippingData
    can_delete = False
    verbose_name_plural = 'Shipping Data'

class ShippingDetailsInline(admin.StackedInline):
    model = ShippingDetails
    can_delete = False
    verbose_name_plural = 'Shipping Details'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount_cents', 'currency', 'merchant_order_id', 'delivery_needed')
    search_fields = ('user__username', 'merchant_order_id')
    list_filter = ('currency', 'delivery_needed')
    inlines = [ItemInline, ShippingDataInline, ShippingDetailsInline]

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'amount_cents', 'quantity')
    search_fields = ('name', 'order__merchant_order_id')
    list_filter = ('order__currency',)

@admin.register(ShippingData)
class ShippingDataAdmin(admin.ModelAdmin):
    list_display = ('order', 'first_name', 'last_name', 'phone_number', 'city', 'country')
    search_fields = ('first_name', 'last_name', 'order__merchant_order_id')
    list_filter = ('city', 'country')

@admin.register(ShippingDetails)
class ShippingDetailsAdmin(admin.ModelAdmin):
    list_display = ('order', 'number_of_packages', 'weight', 'weight_unit')
    search_fields = ('order__merchant_order_id',)
    list_filter = ('weight_unit',)

@admin.register(TestCard)
class TestCardAdmin(admin.ModelAdmin):
    list_display = ('cardholder_name', 'card_number', 'card_expiry', 'card_cvv', 'status')
    search_fields = ('cardholder_name', 'card_number')
    list_filter = ('status',)
    readonly_fields = ('created_at', 'updated_at')

# Optionally, you can customize the admin site header and title as follows:
admin.site.site_header = "My Project Admin"
admin.site.site_title = "My Project Admin Portal"
admin.site.index_title = "Welcome to the Admin Portal"
