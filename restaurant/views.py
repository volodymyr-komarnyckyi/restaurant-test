from datetime import date

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from restaurant.models import Restaurant, Menu
from restaurant.serializers import (
    RestaurantSerializer,
    MenuSerializer,
)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    @action(
        detail=False,
        url_path="get-today-menu",
        methods=["GET"]
    )
    def current_day_menu(self, request):
        today = date.today()
        menu = Menu.objects.filter(date=today).first()

        if menu:
            serializer = MenuSerializer(menu)
            return Response(serializer.data)
        else:
            return Response({'message': 'No menu available for today'}, status=404)
