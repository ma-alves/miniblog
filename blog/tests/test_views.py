from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from ..models import Post, Author, Comment


class TestAuthorListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_authors = 15

        for user_id in range(number_of_authors):
            User.objects.create_user(
                username = f'Jesus{str(user_id)}',
                password = '#Judas666'
            )

    def test_author_list_by_url(self):
        response = self.client.get('/blog/authors/', follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_author_list_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/authors.html')
    
    def test_pagination_is_ten(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 10)

    def test_next_pagination_page(self):
        response = self.client.get(reverse('authors') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 5)

    # pk escolhido para teste aleatoriamente pois os id's são bagunçados
    def test_author_detail_by_url(self):
        author = Author.objects.get(pk=7)
        response = self.client.get(author.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_url_author_detail_by_name(self):
        response = self.client.get(reverse('author', kwargs={'pk': 7}))
        self.assertEqual(response.status_code, 200)


class TestPostViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        post_view_user = User.objects.create_user(
            username = 'Jeova',
            password = '#Demonio777'
        )

        number_of_posts = 15

        for post_id in range(number_of_posts):
            Post.objects.create(
                title = f'Post number {post_id}',
                content = f'Content of post number {post_id}',
                author = post_view_user
            )
    
    def test_post_list_by_url(self):
        response = self.client.get('/blog/posts/', follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_post_list_by_name(self):
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code, 200)

    def test_post_list_uses_correct_template(self):
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/posts.html')

    # Fazer testes de pagination, remover detail view tests dessa classe
        

class TestCreatePost(TestCase):
    def setUp(self):
        # Usuário com permissão
        self.user_with_perm = User.objects.create_user(
            username='HasPerm',
            password='#Parapapa555'
        )
        permission = Permission.objects.get(codename='creator')
        self.user_with_perm.user_permissions.add(permission)
        self.user_with_perm.save()

        # Usuário sem permissão
        self.user_without_perm = User.objects.create_user(
            username='NoPerm',
            password='#Parapapa555'
        )
        self.user_without_perm.save()

    def test_user_with_perm_can_create_post(self):
        login = self.client.login(username='HasPerm', password='#Parapapa555')
        response = self.client.post('/blog/post/create', data={
            'title': 'Create post test title',
            'content': 'Create post test content',
            'author': self.user_with_perm
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_without_perm_cannot_create_post(self):
        login = self.client.login(username='NoPerm', password='#Parapapa555')
        response = self.client.post('/blog/post/create', data={
            'title': 'Create post test title',
            'content': 'Create post test content',
            'author': self.user_without_perm
        })
        self.assertEqual(response.status_code, 403)
