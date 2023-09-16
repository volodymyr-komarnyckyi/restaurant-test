import pytest
from _decimal import Decimal
from django.utils import timezone
from user.models import User
from .models import Restaurant, Menu, Vote
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def create_restaurant():
    return Restaurant.objects.create(
        name="Test Restaurant", description="Test Description"
    )


@pytest.fixture
def create_menu(create_restaurant):
    return Menu.objects.create(
        restaurant=create_restaurant,
        date=timezone.now().date(),
        items="Item 1, Item 2, Item 3",
        price=10.99,
    )


@pytest.fixture
def create_vote(create_menu, user):
    return Vote.objects.create(
        menu=create_menu, employee=user, timestamp=timezone.now()
    )


@pytest.fixture
def user():
    from user.models import User

    return User.objects.create_user(
        email="test@user.com", password="testpassword"
    )


@pytest.mark.django_db
def test_create_restaurant(create_restaurant):
    restaurant = Restaurant.objects.get(name="Test Restaurant")
    assert restaurant.name == "Test Restaurant"
    assert restaurant.description == "Test Description"


@pytest.mark.django_db
def test_create_menu(create_menu):
    menu = Menu.objects.get(restaurant__name="Test Restaurant")
    assert menu.restaurant.name == "Test Restaurant"
    assert menu.items == "Item 1, Item 2, Item 3"
    assert menu.price == Decimal("10.99")


@pytest.mark.django_db
def test_create_vote(create_vote):
    vote = Vote.objects.get(employee__email="test@user.com")
    assert vote.menu.restaurant.name == "Test Restaurant"
    assert vote.employee.email == "test@user.com"


@pytest.mark.django_db
def test_create_user(user):
    assert user.email == "test@user.com"
    assert user.check_password("testpassword")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    user = User.objects.create_user(
        email="test@user.com", password="testpassword"
    )
    return user


# @pytest.fixture
# def create_restaurant():
#     restaurant = Restaurant.objects.create(
#         name="Test Restaurant", description="Test Description"
#     )
#     return restaurant


# @pytest.fixture
# def create_menu(create_restaurant):
#     menu = Menu.objects.create(
#         restaurant=create_restaurant,
#         date=date.today(),
#         items="Item 1, Item 2, Item 3",
#         price=10.99,
#     )
#     return menu


@pytest.mark.django_db
def test_get_today_menu(api_client, create_menu):
    url = "/api/restaurant/menus/get-today-menu/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["restaurant"] == create_menu.restaurant.id


@pytest.mark.django_db
def test_vote_unauthenticated(api_client, create_menu):
    url = f"/api/restaurant/menus/{create_menu.id}/vote/"
    response = api_client.post(url, data={})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_results(api_client, create_menu):
    url = f"/api/restaurant/menus/{create_menu.id}/results/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["menu"] == create_menu.id
    assert response.data["vote_count"] == 0
