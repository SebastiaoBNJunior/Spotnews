from django.test import TestCase
from django.urls import reverse
from news.models import User
from news.models import Category, News
from tests.utils.date_converter import date_converter
from bs4 import BeautifulSoup
from django.conf import settings
import pytest


@pytest.mark.dependency(scope="class")
class HomePageTemplateTest(TestCase):
    def setUp(self):
        User.objects.create(
            name="Yarpen Zigrin",
            email="yarpen.zigrin@gmail.com",
            password="123456",
            role="user",
        )
        User.objects.create(
            name="Camila Silva",
            email="camila.silva@exemplo.com",
            password="senha123",
            role="user",
        )

        category1 = Category.objects.create(name="Tecnologia")
        category2 = Category.objects.create(name="Esportes")
        category3 = Category.objects.create(name="Música")

        self.news1 = News.objects.create(
            title="News 1",
            content="Content 1",
            author=User.objects.get(name="Yarpen Zigrin"),
            created_at="2023-08-08",
            image="images/image.jpg",
        )

        self.news2 = News.objects.create(
            title="News 2",
            content="Content 2",
            author=User.objects.get(name="Camila Silva"),
            created_at="2023-08-09",
            image="images/image2.jpg",
        )
        self.news1.categories.add(category1)
        self.news2.categories.add(category2, category3)

        self.response = self.client.get(reverse("home-page"))
        self.soup = BeautifulSoup(self.response.content, "html.parser")

    def test_home_page_template_rendering(self):
        self.assertTemplateUsed(self.response, "home.html")

    def test_home_template_static_file_loading(self):
        css = self.soup.find("link", {"rel": "stylesheet"})
        self.assertTrue(css)
        self.assertEqual(
            css.get("href"),  # type: ignore
            f"{settings.STATIC_URL}css/style.css",
        )

    def test_home_template_navigation_link(self):
        ul = self.soup.find("ul", {"class": "header-links"})
        self.assertTrue(ul)
        self.assertTrue(ul.a)  # type: ignore
        self.assertEqual(
            ul.a.get("href"),  # type: ignore
            reverse("home-page"),
        )
        self.assertEqual(ul.a.text, "Home")  # type: ignore

    def test_home_template_title_block(self):
        self.assertContains(
            self.response, "<title> Página Inicial </title>", html=True
        )

    def test_home_template_header_block(self):
        header = self.soup.find("header")
        self.assertTrue(header)
        self.assertEqual(header.get("class")[0], "header")  # type: ignore

        self.assertTrue(header.ul)  # type: ignore
        self.assertEqual(
            header.ul.get("class")[0],  # type: ignore
            "header-links",
        )

    def test_home_page_news_cards(self):
        self.assertContains(
            self.response, '<h2 class="news-title">News 1</h2>', html=True
        )
        self.assertContains(
            self.response, '<h2 class="news-title">News 2</h2>', html=True
        )
        self.assertContains(self.response, '<span class="news-date">', count=2)

    def test_home_page_news_images(self):
        image = self.soup.find_all("img")

        self.assertTrue(image[0])
        self.assertEqual(
            image[0].get("src"),
            f"{settings.STATIC_URL[:-1]}{self.news1.image.url}",
        )

        self.assertTrue(image[1])
        self.assertEqual(
            image[1].get("src"),
            f"{settings.STATIC_URL[:-1]}{self.news2.image.url}",
        )

    def test_home_page_news_date_format(self):
        formatted_date1 = date_converter(self.news1.created_at)
        self.assertContains(self.response, f"{formatted_date1}", html=True)

        formatted_date2 = date_converter(self.news2.created_at)
        self.assertContains(self.response, f"{formatted_date2}", html=True)

    @pytest.mark.dependency(
        depends=[
            "HomePageTemplateTest::test_home_page_template_rendering",
            "HomePageTemplateTest::test_home_template_static_file_loading",
            "HomePageTemplateTest::test_home_template_navigation_link",
            "HomePageTemplateTest::test_home_template_title_block",
            "HomePageTemplateTest::test_home_template_header_block",
            "HomePageTemplateTest::test_home_page_news_cards",
            "HomePageTemplateTest::test_home_page_news_images",
            "HomePageTemplateTest::test_home_page_news_date_format",
        ]
    )
    def test_validate_final_home_template(self):
        pass
