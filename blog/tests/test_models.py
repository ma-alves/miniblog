from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Post, Author, Comment

"""Tem uma certa bagunça na criação dos usuários: 
- Os dados são criados em ordem alfabetica de acordo com o nome da classe do
teste, logo devo prestar atenção nos id's dos objetos criados e fazer sua
relação, e et ceteras...
"""


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="TestingUser", password="#HYAhaha5454")

    def test_author_str_is_username(self):
        user = User.objects.get(id=1)
        author = Author.objects.get(id=1)
        self.assertEqual(str(author), user.username)

    def test_author_id_is_user_id(self):
        user = User.objects.get(id=1)
        author = Author.objects.get(id=1)
        self.assertEqual(author.id, user.id)

    def test_author_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), "/blog/author/1")

    def test_bio_label(self):
        author = Author.objects.get(id=1)
        bio_label = author._meta.get_field("bio").verbose_name
        self.assertEqual(bio_label, "bio")

    def test_bio_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field("bio").max_length
        self.assertEqual(max_length, 50)

    def test_bio_content(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.bio, "")


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="TestingUser3", password="#TGRubhs8745"
        )
        post = Post.objects.create(
            title="Test title.",
            content="Test content and stuff and la di da...",
            author=user,
        )

    def test_post_content_length(self):
        post = Post.objects.get(id=2)
        max_length = post._meta.get_field("content").max_length
        self.assertEqual(max_length, 2000)

    def test_post_absolute_url(self):
        post = Post.objects.get(id=2)
        self.assertEqual(post.get_absolute_url(), "/blog/post/2")

    def test_foreign_key_is_user_id(self):
        post = Post.objects.get(id=2)
        user = User.objects.get(id=3)
        self.assertEqual(post.author_id, user.id)

    def test_author_link_matches_user_link(self):
        post = Post.objects.get(id=2)
        user = User.objects.get(id=3)
        self.assertEqual(
            post.author.author.get_absolute_url(), user.author.get_absolute_url()
        )


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="TestingUser2", password="#TUYAoayw123"
        )
        commented_post = Post.objects.create(
            title="Comment test", content="Testing", author=user
        )
        comment = Comment.objects.create(
            content="Comment content", comment_author=user, main_post=commented_post
        )

    def test_comment_content_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field("content").max_length
        self.assertEqual(max_length, 250)

    def test_comment_foreign_key_is_user_id(self):
        post = Comment.objects.get(id=1)
        user = User.objects.get(id=2)
        self.assertEqual(post.comment_author.id, user.id)

    def test_comment_author_link_matches_user_link(self):
        post = Comment.objects.get(id=1)
        user = User.objects.get(id=2)
        self.assertEqual(
            post.comment_author.author.get_absolute_url(),
            user.author.get_absolute_url(),
        )
