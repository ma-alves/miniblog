from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Post, Author


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='TestingUser', password='#HYAhaha5454')

    def test_author_str_is_username(self):
        user = User.objects.get(id=1)
        expected_username = user.username
        author = Author.objects.get(id=1)
        self.assertEqual(str(author), expected_username)

    def test_author_id_is_user_id(self):
        user = User.objects.get(id=1)
        expected_id = user.id
        author = Author.objects.get(id=1)
        self.assertEqual(author.id, expected_id)

    def test_author_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), '/blog/author/1')

    def test_bio_label(self):
        author = Author.objects.get(id=1)
        bio_label = author._meta.get_field('bio').verbose_name
        self.assertEqual(bio_label, 'bio')
    
    def test_bio_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('bio').max_length
        self.assertEqual(max_length, 50)


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='TestingUser2', password='#TGRubhs8745')
        Post.objects.create(
            title = 'Test title.',
            content = 'Test content and stuff and la di da...',
            author = user
        )

    def test_post_content_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('content').max_length
        self.assertEqual(max_length, 2000)        

    def test_post_absolute_url(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.get_absolute_url(), '/blog/post/1')

    def test_foreign_key_is_user_id(self):
        post = Post.objects.get(id=1)
        user = User.objects.get(id=2)
        self.assertEqual(post.author_id, user.id)

    def test_author_link_matches_user_link(self):
        post = Post.objects.get(id=1)
        user = User.objects.get(id=2)
        self.assertEqual(post.author.author.get_absolute_url(), user.author.get_absolute_url())
    