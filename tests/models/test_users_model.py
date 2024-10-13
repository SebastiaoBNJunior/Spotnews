from django.test import TestCase
from django.core.exceptions import ValidationError
from news.models import User
import pytest


@pytest.mark.dependency(scope="class")
class UserModelTestCase(TestCase):
    def test_user_creation(self):
        user = User.objects.create(
            name="Yarpen Zigrin",
            email="yarpen.zigrin@gmail.com",
            password="123456",
            role="user",
        )

        self.assertEqual(user.name, "Yarpen Zigrin")
        self.assertEqual(user.email, "yarpen.zigrin@gmail.com")
        self.assertEqual(user.password, "123456")
        self.assertEqual(user.role, "user")

    def test_user_str_method(self):
        user = User.objects.create(
            name="Yarpen Zigrin",
            email="yarpen.zigrin@gmail.com",
            password="123456",
            role="user",
        )
        self.assertEqual(str(user), "Yarpen Zigrin")

    def test_user_name_field_class(self):
        field = User._meta.get_field("name")
        self.assertEqual(field.__class__.__name__, "CharField")

    def test_user_email_field_class(self):
        field = User._meta.get_field("email")
        self.assertEqual(field.__class__.__name__, "EmailField")

    def test_user_role_field_class(self):
        field = User._meta.get_field("role")
        self.assertEqual(field.__class__.__name__, "CharField")

    def test_user_password_field_class(self):
        field = User._meta.get_field("password")
        self.assertEqual(field.__class__.__name__, "CharField")

    def test_user_name_max_length_property(self):
        max_length = User._meta.get_field("name").max_length
        self.assertEqual(max_length, 200)

    def test_user_email_max_length_property(self):
        max_length = User._meta.get_field("email").max_length
        self.assertEqual(max_length, 200)

    def test_user_password_max_length_property(self):
        max_length = User._meta.get_field("password").max_length
        self.assertEqual(max_length, 200)

    def test_user_role_max_length_property(self):
        max_length = User._meta.get_field("role").max_length
        self.assertEqual(max_length, 200)

    def test_user_name_min_length(self):
        with self.assertRaises(ValidationError) as context:
            user = User.objects.create(
                name="",
                email="test@exemplo.com",
                password="testpassword",
                role="user",
            )
            user.full_clean()
        self.assertEqual(
            str(context.exception),
            "{'name': ['Este campo não pode estar vazio.']}",
        )

    def test_user_name_max_length(self):
        with self.assertRaises(ValidationError) as context:
            user = User(
                name="a" * 201,
                email="test@exemplo.com",
                password="testpassword",
                role="user",
            )
            user.full_clean()
        error_message_dict = context.exception.message_dict
        self.assertIn("name", error_message_dict)
        self.assertEqual(
            error_message_dict["name"][0],
            "Certifique-se de que o valor tenha no máximo 200 caracteres (ele possui 201).", # noqa
        )

    def test_user_email_min_length(self):
        with self.assertRaises(ValidationError) as context:
            user = User.objects.create(
                name="Test User",
                email="",
                password="testpassword",
                role="user",
            )
            user.full_clean()
        self.assertEqual(
            str(context.exception),
            "{'email': ['Este campo não pode estar vazio.']}",
        )

    def test_user_email_max_length(self):
        with self.assertRaises(ValidationError) as context:
            prefix = "a" * 192
            suffix = "@test.com"
            user = User(
                name="Test User",
                email=prefix + suffix,
                password="testpassword",
                role="user",
            )
            user.full_clean()
        error_message_dict = context.exception.message_dict
        self.assertIn("email", error_message_dict)
        self.assertEqual(
            error_message_dict["email"][0],
            "Certifique-se de que o valor tenha no máximo 200 caracteres (ele possui 201).", # noqa
        )

    def test_user_password_min_length(self):
        with self.assertRaises(ValidationError) as context:
            user = User.objects.create(
                name="Test User",
                email="test@exemplo.com",
                password="",
                role="user",
            )
            user.full_clean()
        self.assertEqual(
            str(context.exception),
            "{'password': ['Este campo não pode estar vazio.']}",
        )

    def test_user_password_max_length(self):
        with self.assertRaises(ValidationError) as context:
            user = User(
                name="Test User",
                email="test@exemplo.com",
                password="a" * 201,
                role="user",
            )
            user.full_clean()
        error_message_dict = context.exception.message_dict
        self.assertIn("password", error_message_dict)
        self.assertEqual(
            error_message_dict["password"][0],
            "Certifique-se de que o valor tenha no máximo 200 caracteres (ele possui 201).", # noqa
        )

    def test_user_role_min_length(self):
        with self.assertRaises(ValidationError) as context:
            user = User.objects.create(
                name="Test User",
                email="test@exemplo.com",
                password="testpassword",
                role="",
            )
            user.full_clean()
        self.assertEqual(
            str(context.exception),
            "{'role': ['Este campo não pode estar vazio.']}",
        )

    def test_user_role_max_length(self):
        with self.assertRaises(ValidationError) as context:
            user = User(
                name="Test User",
                email="test@exemplo.com",
                password="testpassword",
                role="a" * 201,
            )
            user.full_clean()
        error_message_dict = context.exception.message_dict
        self.assertIn("role", error_message_dict)
        self.assertEqual(
            error_message_dict["role"][0],
            "Certifique-se de que o valor tenha no máximo 200 caracteres (ele possui 201).", # noqa
        )

    @pytest.mark.dependency(
        depends=[
            "UserModelTestCase::test_user_creation",
            "UserModelTestCase::test_user_name_field_class",
            "UserModelTestCase::test_user_email_field_class",
            "UserModelTestCase::test_user_role_field_class",
            "UserModelTestCase::test_user_password_field_class",
            "UserModelTestCase::test_user_str_method",
            "UserModelTestCase::test_user_name_max_length_property",
            "UserModelTestCase::test_user_email_max_length_property",
            "UserModelTestCase::test_user_password_max_length_property",
            "UserModelTestCase::test_user_role_max_length_property",
            "UserModelTestCase::test_user_name_min_length",
            "UserModelTestCase::test_user_name_max_length",
            "UserModelTestCase::test_user_email_min_length",
            "UserModelTestCase::test_user_email_max_length",
            "UserModelTestCase::test_user_password_min_length",
            "UserModelTestCase::test_user_password_max_length",
            "UserModelTestCase::test_user_role_min_length",
            "UserModelTestCase::test_user_role_max_length",
        ]
    )
    def test_validate_final_user_model(self):
        pass
