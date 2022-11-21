import shutil

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.models import Group, Post, User

from . import consts


@override_settings(MEDIA_ROOT=consts.MEDIA_ROOT)
class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.user = User.objects.create_user(username='Buggy_NaMe')
        cls.group = Group.objects.create(
            title='Баг группа',
            slug='Bug-slug',
            description='Группа багов',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Баг text char15 Видишь это - ищи ошибку!',
            group=cls.group,
            image=uploaded,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(consts.MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post_authorized_client(self):
        """Валидная форма создает запись в Post для авторизованного user."""
        post_count = Post.objects.count()
        post_data = {
            'text': 'Баг text char15 Текст для тестирования!',
            'group': PostFormTests.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=post_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse('posts:profile', kwargs={'username': self.user})
        )
        self.assertEqual(Post.objects.count(), post_count + consts.SHIFT)
        self.assertTrue(
            Post.objects.filter(
                id=self.post.id,
                text=self.post.text,
                image=self.post.image,
            ).exists()
        )

    def test_create_edit_authorized_client(self):
        """Валидная форма изменения записи в Post для авторизованного user."""
        post_data = {
            'text': 'Баг text char15 Текст Edit для тестирования!',
            'group': PostFormTests.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={
                'post_id': self.post.id
            }),
            data=post_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse('posts:post_detail', kwargs={
                'post_id': self.post.id
            })
        )
        self.assertTrue(
            Post.objects.filter(
                id=self.post.id,
                text=post_data['text'],
            ).exists()
        )

    def test_create_post_guest_client(self):
        """Валидная форма создания записи Post для guest."""
        post_data = {
            'text': 'Баг text char15 Текст для тестирования!',
            'group': PostFormTests.group.id,
        }
        response = self.guest_client.post(
            reverse('posts:post_create'),
            data=post_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse('users:login') + '?next=/create/'
        )

    def test_create_edit_guest_client(self):
        """Валидная форма изменения записи в Post для guest."""
        post_data = {
            'text': 'Баг text char15 Текст Edit для тестирования!',
            'group': PostFormTests.group.id,
        }
        response = self.guest_client.post(
            reverse('posts:post_edit', kwargs={
                'post_id': self.post.id
            }),
            data=post_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse(
                'users:login'
            ) + f'?next=/posts/{self.post.id}/edit/'
        )

    def test_create_comment_authorized_client(self):
        """Валидная форма создает запись в Post для авторизованного user."""
        post_count = Post.objects.count()
        post_data = {
            'text': 'Баг text char15 Текст для тестирования!',
            'group': PostFormTests.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=post_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse('posts:profile', kwargs={'username': self.user})
        )
        self.assertEqual(Post.objects.count(), post_count + consts.SHIFT)
        self.assertTrue(
            Post.objects.filter(
                id=self.post.id,
                text=self.post.text,
                image=self.post.image,
            ).exists()
        )
