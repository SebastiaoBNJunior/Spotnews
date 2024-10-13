from django.test import TestCase
from news.models import User
from news.serializers import UserSerializer
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
import pytest


@pytest.mark.dependency(scope="class")
class UserViewSetTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            name="Larissa Nunes",
            email="larissanunes@exemplo.com",
            password="letmein",
            role="user",
        )
        self.user2 = User.objects.create(
            name="Diego Alves",
            email="diegoalves@exemplo.com",
            password="zxcvbnm",
            role="user",
        )
        self.user_data = {
            "id": 3,
            "name": "John Doe",
            "email": "john@exemplo.com",
            "password": "securepassword",
            "role": "user",
        }
        self.user = User(**self.user_data)
        self.serializer = UserSerializer(instance=self.user)

    def test_user_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set(
                [
                    "id",
                    "name",
                    "email",
                    "role",
                ]
            ),
        )

    def test_user_serializer_field_values(self):
        data = self.serializer.data
        self.assertEqual(data["id"], self.user_data["id"])
        self.assertEqual(data["name"], self.user_data["name"])
        self.assertEqual(data["email"], self.user_data["email"])
        self.assertEqual(data["role"], self.user_data["role"])

        self.assertTrue("password" not in data)

    def test_user_viewset_list(self):
        response = self.client.get("/api/users/")

        first_user = {**response.data[0]}  # type: ignore

        second_user = {**response.data[1]}  # type: ignore

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(first_user["id"], self.user1.id)  # type: ignore
        self.assertEqual(first_user["name"], self.user1.name)
        self.assertEqual(first_user["email"], self.user1.email)
        self.assertEqual(first_user["role"], self.user1.role)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(second_user["id"], self.user2.id)  # type: ignore
        self.assertEqual(second_user["name"], self.user2.name)
        self.assertEqual(second_user["email"], self.user2.email)
        self.assertEqual(second_user["role"], self.user2.role)

    def test_user_viewset_create(self):
        data = {
            "name": "Rafaela Santos",
            "email": "rafaelasantos@exemplo.com",
            "password": "p@ssw0rd",
            "role": "user",
        }

        response = self.client.post("/api/users/", data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(
            User.objects.last().name,  # type: ignore
            "Rafaela Santos",
        )
        self.assertEqual(
            User.objects.last().email,  # type: ignore
            "rafaelasantos@exemplo.com",
        )

    def test_end_to_end_user_endpoint(self):
        response = self.client.get("/api/users/")

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            response.json()[0], UserSerializer(instance=self.user1).data
        )
        self.assertEqual(
            response.json()[1], UserSerializer(instance=self.user2).data
        )

        response = self.client.post("/api/users/", self.user_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        response = self.client.get("/api/users/")

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            response.json()[-1], UserSerializer(User.objects.last()).data
        )

    @pytest.mark.dependency(
        depends=[
            "UserViewSetTest::test_user_serializer_contains_expected_fields",
            "UserViewSetTest::test_user_serializer_field_values",
            "UserViewSetTest::test_user_viewset_list",
            "UserViewSetTest::test_user_viewset_create",
            "UserViewSetTest::test_end_to_end_user_endpoint",
        ]
    )
    def test_validate_final_user_drf(self):
        pass
