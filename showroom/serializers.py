from rest_framework import serializers
from .models import Motorcycle, Inventory

class MotorcycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorcycle
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    motorcycle_detail = MotorcycleSerializer(source='motorcycle', read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'