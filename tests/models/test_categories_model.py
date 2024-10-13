from django.test import TestCase
from django.core.exceptions import ValidationError
from news.models import Category
import pytest


@pytest.mark.dependency(scope="class")
class CategoryModelTestCase(TestCase):
    def test_category_name_field_class(self):
        field = Category._meta.get_field("name")
        self.assertEqual(field.__class__.__name__, "CharField")

    def test_category_creation(self):
        category = Category.objects.create(name="Fantasia")
        self.assertEqual(category.name, "Fantasia")

    def test_category_name_max_length_property(self):
        max_length = Category._meta.get_field("name").max_length
        self.assertEqual(max_length, 200)

    def test_category_str_method(self):
        category = Category.objects.create(name="Literatura")
        self.assertEqual(str(category), "Literatura")

    def test_category_name_min_length(self):
        category = Category.objects.create(name="")
        with self.assertRaises(ValidationError) as context:
            category.full_clean()
        self.assertEqual(
            str(context.exception),
            "{'name': ['Este campo não pode estar vazio.']}",
        )

    def test_category_name_max_length(self):
        long_name = "a" * 201
        category = Category(name=long_name)
        with self.assertRaises(ValidationError) as context:
            category.full_clean()
        error_message_dict = context.exception.message_dict
        self.assertIn("name", error_message_dict)
        self.assertEqual(
            error_message_dict["name"][0],
            "Certifique-se de que o valor tenha no máximo 200 caracteres (ele possui 201).", # noqa
        )

    @pytest.mark.dependency(
        depends=[
            "CategoryModelTestCase::test_category_name_field_class",
            "CategoryModelTestCase::test_category_creation",
            "CategoryModelTestCase::test_category_name_max_length_property",
            "CategoryModelTestCase::test_category_str_method",
            "CategoryModelTestCase::test_category_name_min_length",
            "CategoryModelTestCase::test_category_name_max_length",
        ]
    )
    def test_validate_final_category_model(self):
        pass
