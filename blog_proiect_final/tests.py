from django.test import TestCase

# Create your tests here.
from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from .models import Post
from django.contrib.auth.models import User


class PostListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Crearea unui utilizator pentru a crea postări
        test_user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        test_user.save()

        # Crearea a 13 postări pentru a fi folosite în teste
        number_of_posts = 13
        for post_id in range(number_of_posts):
            Post.objects.create(
                author=test_user,
                title='Test post ' + str(post_id),
                content='Lorem ipsum dolor sit amet',
            )

    def test_view_url_exists_at_desired_location(self):
        # Verificarea dacă URL-ul căutat există și returnează status-ul 200
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        # Verificarea dacă URL-ul poate fi accesat prin intermediul numelui
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        # Verificarea dacă pagina este afișată folosind template-ul corect
        response = self.client.get(reverse('blog-home'))
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_pagination_is_ten(self):
        # Verificarea dacă paginarea este setată la 10 postări pe pagină
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['post_list']) == 10)

    def test_lists_all_posts(self):
        # Verificarea dacă toate postările sunt afișate pe pagină
        # 13 postări au fost create în SetUpTestData, așadar ar trebui să fie afișate pe două pagini (10 + 3)
        response = self.client.get(reverse('blog-home')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['post_list']) == 3)

