from django.test import TestCase
from django.core.exceptions import ValidationError
from news.models import User
import pytest

from news.models import Category, News


@pytest.mark.dependency(scope="class")
class NewsModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            name="Yarpen Zigrin",
            email="yarpen.zigrin@gmail.com",
            password="123456",
            role="user",
        )
        Category.objects.create(name="Category")

    def test_news_title_field_class(self):
        field = News._meta.get_field("title")
        self.assertEqual(field.__class__.__name__, "CharField")

    def test_news_content_field_class(self):
        field = News._meta.get_field("content")
        self.assertEqual(field.__class__.__name__, "TextField")

    def test_news_author_field_class(self):
        field = News._meta.get_field("author")
        self.assertEqual(field.__class__.__name__, "ForeignKey")

    def test_news_created_at_field_class(self):
        field = News._meta.get_field("created_at")
        self.assertEqual(field.__class__.__name__, "DateField")

    def test_news_image_field_class(self):
        field = News._meta.get_field("image")
        self.assertEqual(field.__class__.__name__, "ImageField")

    def test_news_category_class(self):
        field = News._meta.get_field("categories")
        self.assertEqual(field.__class__.__name__, "ManyToManyField")

    def test_news_creation(self):
        news = News.objects.create(
            title="Test title",
            content="Test content",
            author=User.objects.get(name="Yarpen Zigrin"),
            created_at="2023-08-08",
            image="images/image.jpg",
        )

        category = Category.objects.get(name="Category")
        news.categories.add(category)

        self.assertEqual(news.title, "Test title")
        self.assertEqual(news.content, "Test content")
        self.assertEqual(news.author.id, self.author.id)  # type: ignore
        self.assertEqual(news.created_at, "2023-08-08")
        self.assertEqual(news.image, "images/image.jpg")
        self.assertEqual(news.categories.get().name, "Category")

    def test_news_str_method(self):
        news = News.objects.create(
            title="Test title",
            content="Test content",
            author=User.objects.get(name="Yarpen Zigrin"),
            created_at="2023-08-08",
            image="images/image.jpg",
        )
        self.assertEqual(str(news), "Test title")

    def test_news_title_max_length_property(self):
        max_length = News._meta.get_field("title").max_length
        self.assertEqual(max_length, 200)

    def test_news_title_min_length(self):
        news = News(
            title="",
            content="Test content",
            author=User.objects.get(name="Yarpen Zigrin"),
            created_at="2023-08-08",
        )
        with self.assertRaises(ValidationError) as context:
            news.full_clean()
        self.assertEqual(
            str(context.exception),
            "{'title': ['Este campo não pode estar vazio.']}",
        )

    def test_news_title_max_length(self):
        news = News(
            title="A " * 101,
            content="Test content",
            author=User.objects.get(name="Yarpen Zigrin"),
            created_at="2023-08-08",
        )
        with self.assertRaises(ValidationError) as context:
            news.full_clean()
        error_message_dict = context.exception.message_dict
        self.assertIn("title", error_message_dict)
        self.assertEqual(
            error_message_dict["title"][0],
            "Certifique-se de que o valor tenha no máximo 200 caracteres (ele possui 202).",  # noqa
        )

    def test_news_title_word_count(self):
        news = News(
            title="UmaUnicaPalavra",
            content="Test content",
            author=User.objects.get(name="Yarpen Zigrin"),
            created_at="2023-08-08",
        )
        with self.assertRaises(ValidationError) as context:
            news.full_clean()
        error_message_dict = context.exception.message_dict
        self.assertIn("title", error_message_dict)
        self.assertEqual(
            error_message_dict["title"][0],
            "O título deve conter pelo menos 2 palavras.",
        )

    def test_news_content_min_length(self):
        news = News(
            title="Test news",
            content="",
            author=User.objects.get(name="Yarpen Zigrin"),
            created_at="2023-08-08",
        )
        with self.assertRaises(ValidationError) as context:
            news.full_clean()
        self.assertEqual(
            str(context.exception),
            "{'content': ['Este campo não pode estar vazio.']}",
        )

    def test_news_created_at_validation(self):
        news = News(
            title="Test title",
            content="Test content",
            author=User.objects.get(name="Yarpen Zigrin"),
            created_at="invalid_date",
        )
        with self.assertRaises(ValidationError) as context:
            news.full_clean()
        self.assertEqual(
            str(context.exception),
            "{'created_at': ['O valor \"invalid_date\" tem um formato de data inválido. Deve ser no formato  YYYY-MM-DD.']}",  # noqa
        )

    def test_news_created_at_future_date(self):
        news = News(
            title="Test title",
            content="Test content",
            author=User.objects.get(name="Yarpen Zigrin"),
            created_at="10-07-2060",
        )
        with self.assertRaises(ValidationError) as context:
            news.full_clean()
        self.assertEqual(
            str(context.exception),
            "{'created_at': ['O valor \"10-07-2060\" tem um formato de data inválido. Deve ser no formato  YYYY-MM-DD.']}",  # noqa
        )

    @pytest.mark.dependency(
        depends=[
            "NewsModelTestCase::test_news_title_field_class",
            "NewsModelTestCase::test_news_content_field_class",
            "NewsModelTestCase::test_news_author_field_class",
            "NewsModelTestCase::test_news_created_at_field_class",
            "NewsModelTestCase::test_news_image_field_class",
            "NewsModelTestCase::test_news_category_class",
            "NewsModelTestCase::test_news_creation",
            "NewsModelTestCase::test_news_str_method",
            "NewsModelTestCase::test_news_title_max_length_property",
            "NewsModelTestCase::test_news_title_min_length",
            "NewsModelTestCase::test_news_title_max_length",
            "NewsModelTestCase::test_news_title_word_count",
            "NewsModelTestCase::test_news_content_min_length",
            "NewsModelTestCase::test_news_created_at_validation",
            "NewsModelTestCase::test_news_created_at_future_date",
        ]
    )
    def test_validate_final_news_model(self):
        pass
