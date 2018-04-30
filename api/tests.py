from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from restaurants.models import Restaurant
from .views import (
    RestaurantListView,
    RestaurantDetailView,
    RestaurantCreateView,
    RestaurantUpdateView,
    RestaurantDeleteView,
)

class RestaurantAPITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create(
            username="bob",
            password='adminadmin',
            is_staff=True,
            )
        self.user.set_password(self.user.password)
        self.user.save()
        self.user2 = User.objects.create(
            username="bob2",
            password='adminadmin',
            )
        self.user2.set_password(self.user2.password)
        self.user2.save()

        self.restaurant_1 = Restaurant.objects.create(
            owner=self.user,
            name="Restaurant 1",
            description="This is Restaurant 1",
            opening_time="00:01:00",
            closing_time="23:59:00",
            logo="http://icons.veryicon.com/png/Movie%20%26%20TV/Free%20Star%20Wars/Darth%20Vader.png"
            )
        self.restaurant_2 = Restaurant.objects.create(
            owner=self.user2,
            name="Restaurant 2", 
            description="This is Restaurant 2",
            opening_time="00:01:00",
            closing_time="23:59:00",
            logo="http://icons.veryicon.com/png/Movie%20%26%20TV/Free%20Star%20Wars/Darth%20Vader.png"
            )

        self.restaurant_data = {
            "owner":self.user,
            "name":"Restaurant 1", 
            "description":"This is Restaurant 1 updated",
            "opening_time":"00:01:00",
            "closing_time":"23:59:00",
        }

    def test_restaurant_list_view(self):
        list_url = reverse("api-list")
        request = self.factory.get(list_url)
        response = RestaurantListView.as_view()(request)
        self.assertEqual(
            [
                {
                    'name':self.restaurant_1.name,
                    'opening_time': self.restaurant_1.opening_time,
                    'closing_time': self.restaurant_1.closing_time,
                },
                {
                    'name':self.restaurant_2.name,
                    'opening_time': self.restaurant_2.opening_time,
                    'closing_time': self.restaurant_2.closing_time,
                },
            ],
            response.data
        )
        self.assertEqual(response.status_code, 200)

    def test_restaurant_detail_view(self):
        detail_url = reverse("api-detail", kwargs = {"restaurant_id": self.restaurant_1.id})
        request = self.factory.get(detail_url)
        response = RestaurantDetailView.as_view()(request, restaurant_id=self.restaurant_1.id)
        self.assertEqual(
            {
                'id':self.restaurant_1.id,
                'owner':self.restaurant_1.owner.id,
                'name':self.restaurant_1.name,
                'description':self.restaurant_1.description,
                'opening_time': self.restaurant_1.opening_time,
                'closing_time': self.restaurant_1.closing_time,
            },
            response.data
        )
        self.assertEqual(response.status_code, 200)

    def test_create_view(self):
        create_url = reverse("api-create")
        request = self.factory.post(create_url, data=self.restaurant_data)

        force_authenticate(request, user=self.user)
        response = RestaurantCreateView.as_view()(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Restaurant.objects.count(), 3)

    def test_restaurant_update_view(self):
        update_url = reverse("api-update", kwargs = {"restaurant_id": self.restaurant_1.id})
        request = self.factory.put(update_url, data=self.restaurant_data)
        response = RestaurantUpdateView.as_view()(request, restaurant_id=self.restaurant_1.id)
        self.assertEqual(response.status_code, 200)

    def test_restaurant_delete_view(self):
        delete_url = reverse("api-delete", kwargs = {"restaurant_id": self.restaurant_1.id})
        request = self.factory.delete(delete_url)
        response1 = RestaurantDeleteView.as_view()(request, restaurant_id=self.restaurant_1.id)
        self.assertEqual(response1.status_code, 204)