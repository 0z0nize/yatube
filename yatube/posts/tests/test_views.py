import shutil
from time import sleep

from django import forms
from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.models import Group, Post, User

from . import consts


@override_settings(MEDIA_ROOT=consts.MEDIA_ROOT)
class PostViewTests(TestCase):
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
        cls.user_t = User.objects.create_user(username='TeSt_NaMe')
        cls.group = Group.objects.create(
            title='Баг группа',
            slug='Bug-slug',
            description='Группа любителей багов',
        )
        cls.group_t = Group.objects.create(
            title='Тест группа',
            slug='test-slug',
            description='Группа тестировщиков',
        )
        cls.post_t = Post.objects.create(
            author=cls.user_t,
            text='Баг text char15 Текст для тестирования!',
            group=cls.group_t,
        )
        sleep(consts.DELAY)
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
        self.authorized_client_t = Client()
        self.authorized_client_t.force_login(self.user_t)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        cache.clear()
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={
                'slug': self.group.slug
            }): 'posts/group_list.html',
            reverse('posts:profile', kwargs={
                'username': self.user
            }): 'posts/profile.html',
            reverse('posts:post_detail', kwargs={
                'post_id': self.post.id
            }): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit', kwargs={
                'post_id': self.post.id
            }): 'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    @staticmethod
    def context_test(f_p, self):
        check_list = [
            self.assertEqual(f_p.text, self.post.text),
            self.assertEqual(f_p.author, self.user),
            self.assertEqual(f_p.image, self.post.image),
            self.assertEqual(f_p.group.title, self.group.title),
            self.assertEqual(f_p.group.slug, self.group.slug),
            self.assertEqual(f_p.group.description, self.group.description)
        ]
        for check in check_list:
            test = check
        return test

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        cache.clear()
        response = self.authorized_client.get(reverse('posts:index'))
        first_post = response.context['page_obj'][consts.ZERO]
        self.context_test(first_post, self)

    def test_group_list_show_correct_context(self):
        """Шаблон posts/group_list.html сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        first_post = response.context['page_obj'][consts.ZERO]
        self.context_test(first_post, self)

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail.html сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        first_post = response.context['post']
        self.context_test(first_post, self)

    def test_post_profile_show_correct_context(self):
        """Шаблон posts/profile.html сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user})
        )
        first_post = response.context['page_obj'][consts.ZERO]
        self.context_test(first_post, self)
        self.assertEqual(
            first_post.author.posts.count(), self.post.author.posts.count()
        )

    def test_create_post_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id})
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_with_group_in_self_group_list(self):
        """Тест, пост не попал в группу, для которой не был предназначен."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        first_post = response.context['page_obj'][consts.ZERO]
        self.assertNotEqual(first_post.text, self.post_t.text)
        self.assertEqual(first_post.author, self.user)
        self.assertNotEqual(first_post.group.title, self.group_t.title)
        self.assertNotEqual(first_post.group.slug, self.group_t.slug)
        self.assertNotEqual(
            first_post.group.description, self.group_t.description
        )

    def test_x_cache_index(self):
        """Тест для проверки кэширования главной страницы"""
        response = self.authorized_client.get(reverse('posts:index'))
        Post.objects.filter(pk=self.post_t.id).delete()
        cache_response = self.authorized_client.get(
            reverse('posts:index')
        )
        self.assertEqual(
            response.content,
            cache_response.content
        )
        cache.clear()
        cache_clear_response = self.authorized_client.get(
            reverse('posts:index')
        )
        self.assertNotEqual(
            response.content,
            cache_clear_response.content
        )

    def test_follow_authorized(self):
        """Авторизованный пользователь может подписываться на
        других пользователей и удалять их из подписок."""
        response = self.authorized_client.get(reverse('posts:follow_index'))
        follow_list_false = response.context['page_obj'].object_list
        self.assertEqual(len(follow_list_false), consts.ZERO)

        self.authorized_client.get(reverse(
            'posts:profile_follow',
            kwargs={'username': self.post_t.author}
        ))
        response = self.authorized_client.get(reverse('posts:follow_index'))
        follow_list_true = response.context['page_obj'].object_list
        self.assertEqual(len(follow_list_true), consts.SHIFT)

        self.authorized_client.get(reverse(
            'posts:profile_unfollow',
            kwargs={'username': self.post_t.author}
        ))
        response = self.authorized_client.get(reverse('posts:follow_index'))
        unfollow_list = response.context['page_obj'].object_list
        self.assertEqual(len(unfollow_list), consts.ZERO)

    def test_new_post_appears_in_follow_index(self):
        """Новая запись пользователя появляется в ленте тех,
        кто на него подписан и не появляется в ленте тех, кто не подписан."""
        blogger = User.objects.create_user(username='Blogger_NaMe')
        post = Post.objects.create(
            author=blogger,
            text='Баг text follow!',
            group=self.group,
        )
        self.authorized_client.get(reverse(
            'posts:profile_follow',
            kwargs={'username': post.author}
        ))
        response = self.authorized_client.get(reverse('posts:follow_index'))
        self.assertIn(post, response.context['page_obj'].object_list)
        response_t = self.authorized_client_t.get(
            reverse('posts:follow_index')
        )
        self.assertNotIn(post, response_t.context['page_obj'].object_list)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Buggy_NaMe')
        cls.group = Group.objects.create(
            title='Баг группа',
            slug='Bug-slug',
            description='Группа любителей багов',
        )
        for test_n in range(consts.POSTS_FOR_TEST):
            cls.post = Post.objects.create(
                author=cls.user,
                text=f'Баг текс char15 № {test_n} Видишь это - ищи ошибку!',
                group=cls.group,
            )

    def setUp(self):
        self.authorized_client = Client()

    def test_paginator(self):
        """Тест, для проверки пэджинатора."""
        pages = (consts.POSTS_FOR_TEST // settings.POST_IN_PAGE)
        last_page = consts.POSTS_FOR_TEST % settings.POST_IN_PAGE

        list_pages = [
            (
                settings.POST_IN_PAGE, num
            ) for num in range(consts.SHIFT, pages + consts.SHIFT)
        ]
        if last_page:
            last = (last_page, pages + consts.SHIFT)
            list_pages.append(last)
        list_pages
        for page_n in list_pages:
            page_num = page_n[consts.SHIFT]

            url_pages = {
                reverse('posts:index'): page_num,
                reverse(
                    'posts:group_list', kwargs={'slug': self.group.slug}
                ): page_num,
                reverse(
                    'posts:profile', kwargs={'username': self.user}
                ): page_num,
            }
            for reverse_temlate, page in url_pages.items():
                with self.subTest(reverse_temlate=reverse_temlate):
                    response = self.authorized_client.get(
                        reverse_temlate, {'page': page}
                    )
                    self.assertEqual(
                        len(response.context['page_obj']), page_n[consts.ZERO]
                    )
