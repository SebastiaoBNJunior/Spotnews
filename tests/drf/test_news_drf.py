from django.test import TestCase
from news.models import User
from news.models import Category, News
from news.serializers import NewsSerializer
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
import os
from datetime import date
import pytest


@pytest.mark.dependency(scope="class")
class NewsViewSetTest(TestCase):
    def setUp(self):
        self.user_data = {
            "name": "Marcos Farias",
            "email": "marcosf@exemplo.com",
            "password": "senhasupersegura",
            "role": "user",
        }

        self.user = User.objects.create(**self.user_data)
        self.category = Category.objects.create(name="Tecnologia")

        self.news = News.objects.create(
            title="Noticia 1",
            content="Conteúdo 1",
            author=User.objects.get(name="Marcos Farias"),
            created_at="2023-08-08",
            image="/img/image.jpg",
        )

        category = Category.objects.get(name="Tecnologia")
        self.news.categories.add(category)

        self.serializer = NewsSerializer(instance=self.news)

    def test_news_serializer_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = [
            "id",
            "title",
            "content",
            "author",
            "created_at",
            "image",
            "categories",
        ]
        self.assertEqual(set(data.keys()), set(expected_fields))

    def test_news_serializer_field_values(self):
        data = self.serializer.data
        user_id = self.news.author.id  # type: ignore
        image_name = self.news.image.name
        category_id = self.news.categories.all()[0].id
        self.assertEqual(data["id"], self.news.id)  # type: ignore
        self.assertEqual(data["title"], self.news.title)
        self.assertEqual(data["content"], self.news.content)
        self.assertEqual(data["author"], user_id)
        self.assertEqual(data["created_at"], self.news.created_at)
        self.assertEqual(data["image"], image_name)
        self.assertEqual(data["categories"][0], category_id)

    def test_news_viewset_list(self):
        author = User.objects.create(
            name="Camila Rodrigues",
            email="camilarodrigues@exemplo.com",
            password="qazwsx",
            role="user",
        )
        category = Category.objects.create(name="Artesanato")

        news1 = News.objects.create(
            title="Notícia 2",
            content="Conteúdo 2",
            author=User.objects.get(name="Camila Rodrigues"),
            created_at=date(2023, 8, 8),
            image="img/image.jpg",
        )
        news1.categories.add(category)

        news2 = News.objects.create(
            title="Notícia 3",
            content="Conteúdo 3",
            author=User.objects.get(name="Camila Rodrigues"),
            created_at=date(2023, 8, 9),
            image="img/image2.jpg",
        )
        news2.categories.add(category)

        response = self.client.get("/api/news/")

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # type: ignore
        self.assertEqual(
            response.data[1]["title"],  # type: ignore
            "Notícia 2",
        )
        self.assertEqual(
            response.data[2]["title"],  # type: ignore
            "Notícia 3",
        )
        self.assertEqual(
            response.data[1]["content"],  # type: ignore
            "Conteúdo 2",
        )
        self.assertEqual(
            response.data[2]["content"],  # type: ignore
            "Conteúdo 3",
        )
        self.assertEqual(author.id, response.data[1]["author"])  # type: ignore
        self.assertEqual(author.id, response.data[2]["author"])  # type: ignore
        self.assertEqual(
            response.data[1]["created_at"],  # type: ignore
            "2023-08-08",
        )
        self.assertEqual(
            response.data[2]["created_at"],  # type: ignore
            "2023-08-09",
        )
        self.assertIn(
            "image.jpg",
            response.data[1]["image"],  # type: ignore
            "Notícia 1",
        )
        self.assertIn(
            "image2.jpg",
            response.data[2]["image"],  # type: ignore
            "Notícia 2",
        )

    def test_news_viewset_create(self):
        author = User.objects.create(
            name="Ana Oliveira",
            email="anaoliveira@exemplo.com",
            password="987654",
            role="user",
        )
        category = Category.objects.create(name="Cultura POP")

        project_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        image_path = os.path.join(project_dir, "img/avanco-tecnologico.jpg")
        with open(image_path, "rb") as image_file:
            data = {
                "title": "Notícia 4",
                "content": "Conteúdo 4",
                "author": author.id,  # type: ignore
                "created_at": date(2023, 8, 8),
                "image": image_file,
                "categories": [category.id],  # type: ignore
            }

            response = self.client.post("/api/news/", data, format="multipart")

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(News.objects.count(), 2)
        self.assertEqual(
            News.objects.last().title,  # type: ignore
            "Notícia 4",
        )
        self.assertEqual(
            News.objects.last().content,  # type: ignore
            "Conteúdo 4",
        )
        self.assertEqual(
            News.objects.last().author,  # type: ignore
            author,
        )
        self.assertEqual(
            News.objects.last().created_at,  # type: ignore
            date(2023, 8, 8),
        )

        image_url = News.objects.last().image  # type: ignore
        image_to_remove_path = project_dir + "/" + str(image_url)
        os.remove(image_to_remove_path)

    def test_end_to_end_news_endpoint(self):
        response = self.client.get("/api/news/")

        self.assertEqual(response.status_code, HTTP_200_OK)
        expected_news = NewsSerializer(News.objects.get(id=1)).data
        self.assertEqual(response.json()[0]["id"], expected_news["id"])
        self.assertEqual(response.json()[0]["title"], expected_news["title"])
        self.assertEqual(
            response.json()[0]["content"], expected_news["content"]
        )
        self.assertEqual(response.json()[0]["author"], expected_news["author"])
        self.assertEqual(
            response.json()[0]["created_at"], expected_news["created_at"]
        )
        self.assertEqual(
            response.json()[0]["image"],
            f'http://testserver{expected_news["image"]}',
        )

        author = User.objects.create(
            name="Ana Oliveira",
            email="anaoliveira@exemplo.com",
            password="987654",
            role="user",
        )
        category = Category.objects.create(name="Cultura POP")
        project_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        image_path = os.path.join(project_dir, "img/avanco-tecnologico.jpg")
        with open(image_path, "rb") as image_file:
            data = {
                "title": "Notícia 4",
                "content": "Conteúdo 4",
                "author": author.id,  # type: ignore
                "created_at": date(2023, 8, 8),
                "image": image_file,
                "categories": [category.id],  # type: ignore
            }
            response = self.client.post("/api/news/", data)

            self.assertEqual(response.status_code, HTTP_201_CREATED)

            response = self.client.get("/api/news/")

            image_path = "".join(
                [
                    project_dir,
                    "/img/",
                    response.json()[1]["image"].split("/")[-1],
                ]
            )

            self.assertEqual(response.status_code, HTTP_200_OK)
            self.assertEqual(response.json()[1]["title"], data["title"])
            self.assertEqual(response.json()[1]["content"], data["content"])
            self.assertEqual(response.json()[1]["author"], data["author"])
            self.assertEqual(
                response.json()[1]["created_at"],
                data["created_at"].strftime("%Y-%m-%d"),
            )
            self.assertTrue(os.path.isfile(image_path))
            self.assertEqual(
                response.json()[1]["categories"], data["categories"]
            )

            os.remove(image_path)

    @pytest.mark.dependency(
        depends=[
            "NewsViewSetTest::test_news_serializer_contains_expected_fields",
            "NewsViewSetTest::test_news_serializer_field_values",
            "NewsViewSetTest::test_news_viewset_list",
            "NewsViewSetTest::test_news_viewset_create",
            "NewsViewSetTest::test_end_to_end_news_endpoint",
        ]
    )
    def test_validate_final_news_drf(self):
        pass
