from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
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
            text='Баг текс char15 Если ты это видишь - ищи ошибку!',
        )

    def test_group_model_have_correct_object_names(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

    def test_post_model_have_correct_object_names(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        post = PostModelTest.post
        expected_object_name = post.text[:settings.CHAR_IN_TITLE]
        self.assertEqual(expected_object_name, str(post))
