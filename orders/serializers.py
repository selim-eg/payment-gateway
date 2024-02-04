from rest_framework import serializers
from .models import Order, Item, ShippingData, ShippingDetails

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ('order',) 

class ShippingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingData
        exclude = ('order',)  

class ShippingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingDetails
        exclude = ('order',) 

class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    shipping_data = ShippingDataSerializer()
    shipping_details = ShippingDetailsSerializer()

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('user',)
        
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        shipping_data = validated_data.pop('shipping_data')
        shipping_details = validated_data.pop('shipping_details')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            Item.objects.create(order=order, **item_data)
        ShippingData.objects.create(order=order, **shipping_data)
        ShippingDetails.objects.create(order=order, **shipping_details)
        return order


    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        shipping_data = validated_data.pop('shipping_data', None)
        shipping_details = validated_data.pop('shipping_details', None)

        # Update the order instance
        super(OrderSerializer, self).update(instance, validated_data)

        # Update or create items
        if items_data is not None:
            for item_data in items_data:
                item_id = item_data.get('id', None)
                if item_id:
                    item_instance = Item.objects.get(id=item_id, order=instance)
                    for attr, value in item_data.items():
                        setattr(item_instance, attr, value)
                    item_instance.save()
                else:
                    Item.objects.create(order=instance, **item_data)

        # Update shipping data and details
        if shipping_data is not None:
            for attr, value in shipping_data.items():
                setattr(instance.shipping_data, attr, value)
            instance.shipping_data.save()

        if shipping_details is not None:
            for attr, value in shipping_details.items():
                setattr(instance.shipping_details, attr, value)
            instance.shipping_details.save()

        return instance