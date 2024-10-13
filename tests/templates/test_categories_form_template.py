from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup
import pytest


@pytest.mark.dependency(scope="class")
class CategoriesFormTemplateTest(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("categories-form"))
        self.soup = BeautifulSoup(self.response.content, "html.parser")

    def test_categories_form_template_rendering(self):
        self.assertTemplateUsed(self.response, "categories_form.html")

    def test_home_template_title_block(self):
        self.assertContains(
            self.response,
            "<title> Formulário para Nova Categoria </title>",
            html=True,
        )

    def test_categories_form_template_header_block(self):
        header = self.soup.find("header")
        self.assertTrue(header)
        self.assertEqual(header.get("class")[0], "header")  # type: ignore

        self.assertTrue(header.ul)  # type: ignore
        self.assertEqual(
            header.ul.get("class")[0],  # type: ignore
            "header-links",
        )

    def test_categories_form_template_navigation_link(self):
        ul = self.soup.find("ul", {"class": "header-links"})
        a_s = ul.find_all("a")  # type: ignore
        self.assertTrue(ul)
        self.assertTrue(a_s[0])
        self.assertEqual(a_s[0].get("href"), reverse("home-page"))
        self.assertEqual(a_s[0].text, "Home")
        self.assertTrue(a_s[1])
        self.assertEqual(a_s[1].get("href"), reverse("categories-form"))
        self.assertEqual(a_s[1].text, "Cadastrar Categorias")

    def test_categories_tag_form_existence(self):
        form = self.soup.find("form")
        self.assertTrue(form)
        self.assertEqual(form.get("method"), "post")  # type: ignore
        self.assertEqual(
            form.get("action"),  # type: ignore
            reverse("categories-form"),
        )

    def test_categories_form_input(self):
        form_fields = ["Nome"]
        for field_name in form_fields:
            self.assertIn(
                f'<label for="id_name">{field_name}',
                self.response.content.decode(),
            )
            self.assertIn(
                '<input type="text" name="name" maxlength="200" required',
                self.response.content.decode(),
            )

    def test_categories_form_submit_button(self):
        self.assertContains(
            self.response, '<button type="submit">Salvar</button>', html=True
        )

    def test_categories_empty_form(self):
        form = self.response.context["form"]
        self.assertFalse(form.is_bound)

    def test_categories_form_submission(self):
        data = {
            "name": "História Natural",
        }
        post_response = self.client.post(reverse("categories-form"), data)
        self.assertRedirects(post_response, reverse("home-page"))

    def test_csrf_token_input(self):
        csrf = self.soup.find("input", {"type": "hidden"})

        self.assertTrue(csrf)
        self.assertEqual(
            csrf.get("name"),  # type: ignore
            "csrfmiddlewaretoken",
        )

    @pytest.mark.dependency(
        depends=[
            "CategoriesFormTemplateTest::test_categories_form_template_rendering",  # noqa
            "CategoriesFormTemplateTest::test_home_template_title_block",
            "CategoriesFormTemplateTest::test_categories_form_template_header_block",  # noqa
            "CategoriesFormTemplateTest::test_categories_form_template_navigation_link",  # noqa
            "CategoriesFormTemplateTest::test_categories_tag_form_existence",
            "CategoriesFormTemplateTest::test_categories_form_input",
            "CategoriesFormTemplateTest::test_categories_form_submit_button",
            "CategoriesFormTemplateTest::test_categories_empty_form",
            "CategoriesFormTemplateTest::test_categories_form_submission",
            "CategoriesFormTemplateTest::test_csrf_token_input",
        ]
    )
    def test_validate_final_categories_form_template(self):
        pass
