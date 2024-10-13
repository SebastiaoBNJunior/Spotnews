from django.test import TestCase
from django.urls import reverse
import os
from news.models import User
import pytest
from bs4 import BeautifulSoup
from django.conf import settings

from news.models import Category


@pytest.mark.dependency(scope="class")
class NewsFormTemplateTest(TestCase):
    def setUp(self):
        User.objects.create(
            name="Yarpen Zigrin",
            email="yarpen.zigrin@gmail.com",
            password="123456",
            role="user",
        )
        Category.objects.create(name="Fantasia")
        Category.objects.create(name="Natureza")
        category1 = Category.objects.get(name="Fantasia")
        category2 = Category.objects.get(name="Natureza")

        self.user = User.objects.get(name="Yarpen Zigrin")
        self.categories = [category1.id, category2.id]  # type: ignore

        self.response = self.client.get(reverse("news-form"))
        self.soup = BeautifulSoup(self.response.content, "html.parser")

    def test_news_form_template_rendering(self):
        self.assertTemplateUsed(self.response, "news_form.html")

    def test_news_detail_template_title_block(self):
        self.assertContains(
            self.response,
            "<title> Formulário para Nova Notícia </title>",
            html=True,
        )

    def test_news_form_template_header_block(self):
        header = self.soup.find("header")
        self.assertTrue(header)
        self.assertTrue(header.get("class"), "header")  # type: ignore

        self.assertTrue(header.ul)  # type: ignore
        self.assertTrue(header.ul.get("class"), "header-links")  # type: ignore

    def test_news_form_template_navigation_link(self):
        ul = self.soup.find("ul", {"class": "header-links"})
        a_s = ul.find_all("a")  # type: ignore
        self.assertTrue(ul)
        self.assertTrue(a_s[0])
        self.assertTrue(a_s[0].get("href"), reverse("home-page"))
        self.assertTrue(a_s[0].text, "Home")
        self.assertTrue(a_s[1])
        self.assertTrue(a_s[1].get("href"), reverse("categories-form"))
        self.assertTrue(a_s[1].text, "Cadastrar Categorias")
        self.assertTrue(a_s[2])
        self.assertTrue(a_s[2].get("href"), reverse("news-form"))
        self.assertTrue(a_s[2].text, "Cadastrar Notícias")

    def test_news_tag_form_existence(self):
        form = self.soup.find("form")
        self.assertTrue(form)
        self.assertTrue(form.get("method"), "post")  # type: ignore
        self.assertTrue(
            form.get("action"),  # type: ignore
            reverse("news-form"),
        )
        self.assertTrue(
            form.get("enctype"),  # type: ignore
            "multipart/form-data",
        )

    def test_news_form_title_input(self):
        self.assertIn(
            '<label for="id_title">Título',
            self.response.content.decode(),
        )
        self.assertIn(
            '<input type="text" name="title"',
            self.response.content.decode(),
        )

    def test_news_form_content_textarea(self):
        self.assertIn(
            '<label for="id_content">Conteúdo', self.response.content.decode()
        )
        self.assertIn(
            '<textarea name="content"',
            self.response.content.decode(),
        )

    def test_news_form_author_select(self):
        self.assertIn(
            '<label for="id_author">Autoria', self.response.content.decode()
        )
        self.assertIn('<select name="author"', self.response.content.decode())
        self.assertIn("Yarpen Zigrin</option>", self.response.content.decode())

    def test_news_form_created_at_input(self):
        self.assertIn(
            '<label for="id_created_at">Criado em',
            self.response.content.decode(),
        )
        self.assertIn(
            '<input type="date" name="created_at"',
            self.response.content.decode(),
        )

    def test_news_form_image_input(self):
        self.assertIn(
            '<label for="id_image">URL da Imagem',
            self.response.content.decode(),
        )
        self.assertIn(
            '<input type="file" name="image"',
            self.response.content.decode(),
        )

    def test_news_form_categories_input(self):
        self.assertIn(
            '<label for="id_categories_',
            self.response.content.decode(),
        )
        self.assertIn(
            '<input type="checkbox" name="categories"',
            self.response.content.decode(),
        )
        self.assertIn(
            "Fantasia</label>",
            self.response.content.decode(),
        )
        self.assertIn(
            "Natureza</label>",
            self.response.content.decode(),
        )

    def test_news_form_submit_button(self):
        self.assertContains(
            self.response, '<button type="submit">Salvar</button>', html=True
        )

    def test_news_empty_form(self):
        form = self.response.context["form"]
        self.assertFalse(form.is_bound)

    def test_news_form_submission(self):
        k = "KYZz782gw5qGRTsCOlkLqv1ZKDeERIzATzhTsrTnKsUovN6Lut312pWUUCn92j3w"
        project_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        image_path = os.path.join(project_dir, "img/avanco-tecnologico.jpg")

        with open(image_path, "rb") as image_file:
            data = {
                "title": "Exemplo de Título",
                "content": "Conteúdo de exemplo",
                "author": self.user.id,  # type: ignore
                "created_at": "2023-08-09",
                "image": image_file,
                "categories": self.categories,
                "csrfmiddlewaretoken": k,
            }
            post_response = self.client.post(
                reverse("news-form"), data, format="multipart", follow=True
            )

        self.assertRedirects(post_response, reverse("home-page"))
        soup = BeautifulSoup(post_response.content, "html.parser")
        image_url = soup.find("img").get("src")  # type: ignore
        static_url_prefix = len(settings.STATIC_URL[:-1])

        image_to_remove_path = \
            project_dir + image_url[static_url_prefix:]  # type: ignore

        os.remove(image_to_remove_path)

    def test_csrf_token_input(self):
        csrf = self.soup.find("input", {"type": "hidden"})

        self.assertTrue(csrf)
        self.assertEqual(
            csrf.get("name"),  # type: ignore
            "csrfmiddlewaretoken",
        )

    @pytest.mark.dependency(
        depends=[
            "NewsFormTemplateTest::test_news_form_template_rendering",
            "NewsFormTemplateTest::test_news_detail_template_title_block",
            "NewsFormTemplateTest::test_news_form_template_header_block",
            "NewsFormTemplateTest::test_news_form_template_navigation_link",
            "NewsFormTemplateTest::test_news_tag_form_existence",
            "NewsFormTemplateTest::test_news_form_title_input",
            "NewsFormTemplateTest::test_news_form_content_textarea",
            "NewsFormTemplateTest::test_news_form_author_select",
            "NewsFormTemplateTest::test_news_form_created_at_input",
            "NewsFormTemplateTest::test_news_form_image_input",
            "NewsFormTemplateTest::test_news_form_categories_input",
            "NewsFormTemplateTest::test_news_form_submit_button",
            "NewsFormTemplateTest::test_news_empty_form",
            "NewsFormTemplateTest::test_news_form_submission",
            "NewsFormTemplateTest::test_csrf_token_input",
        ]
    )
    def test_validate_final_news_form_template(self):
        pass
