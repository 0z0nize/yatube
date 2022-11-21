from django.test import Client, TestCase


class StaticPagesURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_url_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'about/author.html': '/about/author/',
            'about/tech.html': '/about/tech/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_about_url_exists_at_desired_location(self):
        """Проверка доступности адреса /about/."""
        templates = {
            'tech': '/about/tech/',
            'author': '/about/author/',
        }
        for name, address in templates.items():
            with self.subTest(name=name):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, 200)
