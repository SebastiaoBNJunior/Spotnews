from django.test import TestCase
from rest_framework.test import APIClient
from news.models import Category
from news.serializers import CategorySerializer
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
import pytest


@pytest.mark.dependency(scope="class")
class CategoryDRFTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.category_data = {
            "id": 1,
            "name": "Technology",
        }
        self.category = Category(**self.category_data)
        self.serializer = CategorySerializer(instance=self.category)

    def test_category_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(["id", "name"]))

    def test_category_serializer_field_values(self):
        data = self.serializer.data
        self.assertEqual(data["id"], self.category_data["id"])
        self.assertEqual(data["name"], self.category_data["name"])

    def test_category_viewset_list(self):
        category1 = Category.objects.create(name="Filmes")
        category2 = Category.objects.create(name="Viagens")

        response = self.client.get("/api/categories/")

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            response.data,  # type: ignore
            [
                {"id": category1.id, "name": "Filmes"},  # type: ignore
                {"id": category2.id, "name": "Viagens"},  # type: ignore
            ],
        )

    def test_category_viewset_create(self):
        data = {"name": "Filmes"}

        response = self.client.post("/api/categories/", data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(
            Category.objects.first().name,  # type: ignore
            "Filmes",
        )

    def test_end_to_end_category_endpoint(self):
        response = self.client.get("/api/categories/")

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json(), [])

        response = self.client.post("/api/categories/", self.category_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        response = self.client.get("/api/categories/")

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            response.json()[0]["name"], self.category_data["name"]
        )

    @pytest.mark.dependency(
        depends=[
            "CategoryDRFTest::test_category_serializer_contains_expected_fields",  # noqa
            "CategoryDRFTest::test_category_serializer_field_values",
            "CategoryDRFTest::test_category_viewset_list",
            "CategoryDRFTest::test_category_viewset_create",
            "CategoryDRFTest::test_end_to_end_category_endpoint",
        ]
    )
    def test_validate_final_category_drf(self):
        pass
