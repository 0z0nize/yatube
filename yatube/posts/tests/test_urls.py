from http import HTTPStatus

from django.core.cache import cache
from django.test import Client, TestCase

from posts.models import Group, Post, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Buggy_NaMe')
        cls.group = Group.objects.create(
            title='Баг группа',
            slug='Bug-slug',
            description='Группа любителей багов',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Баг текс char15 Видишь это - ищи ошибку!!',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_url_exists_at_desired_location(self):
        """Проверка доступности страниц неавторизованным пользователям."""
        template_url_names = {
            'index': '/',
            'group_list': f'/group/{self.group.slug}/',
            'profile': f'/profile/{self.user}/',
            'post_detail': f'/posts/{self.post.id}/',
        }
        for name, location in template_url_names.items():
            with self.subTest(name=name):
                response = self.guest_client.get(location)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_exists_at_desired_location_for_author(self):
        """Страница редактирования поста доступна только автору."""
        response = self.authorized_client.get(f'/posts/{self.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_exists_at_desired_location_for_authorized_user(self):
        """Страница создание поста доступна авторизованному пользователю."""
        response = self.guest_client.get('/create/')
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_url_unexisting_page_return_404(self):
        """Проверка запроза к несуществующей странице."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_url_posts_use_correct_template(self):
        """Проверка доступности шаблонов."""
        cache.clear()
        template_url_names = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user}/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            f'/posts/{self.post.id}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
            '/nonexist-page/': 'core/404.html',
        }
        for url, template in template_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
