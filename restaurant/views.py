from datetime import date

from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from restaurant.models import Restaurant, Menu, Vote
from restaurant.serializers import RestaurantSerializer, MenuSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    @action(detail=False, url_path="get-today-menu", methods=["GET"])
    def current_day_menu(self, request):
        today = date.today()
        menu = Menu.objects.filter(date=today).first()

        if menu:
            serializer = MenuSerializer(menu)
            return Response(serializer.data)
        else:
            return Response(
                {"message": "No menu available for today"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=True, url_path="vote", methods=["POST"])
    def vote(self, request, pk=None):
        menu = get_object_or_404(Menu, pk=pk)
        user = request.user

        if not user.is_authenticated:
            return Response(
                {"message": "Authentication required to vote"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        existing_vote = Vote.objects.filter(menu=menu, employee=user).first()
        if existing_vote:
            return Response(
                {"message": "You have already voted for this menu"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_vote = Vote(menu=menu, employee=user, timestamp=now())
        new_vote.save()

        return Response(
            {"message": "Vote recorded successfully"},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, url_path="results", methods=["GET"])
    def results(self, request, pk=None):
        menu = self.get_object()
        today = date.today()
        vote_count = Vote.objects.filter(
            menu=menu, timestamp__date=today
        ).count()

        return Response({"menu": menu.id, "vote_count": vote_count})


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def list(self, request, *args, **kwargs):
        today = date.today()
        restaurants = self.get_queryset()

        restaurant_data = []
        for restaurant in restaurants:
            menu = restaurant.menus.filter(date=today).first()
            if menu:
                menu_data = MenuSerializer(menu).data
            else:
                menu_data = {"message": "No menu available for today"}

            restaurant_data.append(
                {
                    "restaurant": RestaurantSerializer(restaurant).data,
                    "menu": menu_data
                }
            )

        return Response(restaurant_data)

    def retrieve(self, request, *args, **kwargs):
        today = date.today()
        instance = self.get_object()

        menu = instance.menus.filter(date=today).first()
        if menu:
            menu_data = MenuSerializer(menu).data
        else:
            menu_data = {"message": "No menu available for today"}

        serializer = self.get_serializer(instance)
        data = serializer.data
        data["menu"] = menu_data

        return Response(data)
