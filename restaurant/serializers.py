from rest_framework import serializers

from restaurant.models import (
    Restaurant,
    Menu,
)


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"
        extra_kwargs = {"restaurant": {"write_only": True}}


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"
