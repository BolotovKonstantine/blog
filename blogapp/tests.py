from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post

# Create your tests here.


class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@cloit.net',
            password='secret'
        )
        self.post = Post.objects.create(
            title='A good title',
            body='Nice body content',
            author=self.user
        )

    def test_string_representation(self):
        post = Post(title='A sample title')
        self.assertEqual(str(post), post.title)


    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')


    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good title')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'Nice body content')


    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice body content')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'post_detail.html')


    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), {
            'title': 'New Post',
            'body': 'This is a new post',
            'author': self.user
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Post')
        self.assertContains(response, 'This is a new post')


    def test_post_update_view(self):
        response = self.client.post(reverse('post_edit', args='1'), {
            'title': 'Updated Post',
            'body': 'This is an updated post',
        })
        self.assertEqual(response.status_code, 302)


    def test_post_delete_view(self):
        response = self.client.get(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 200)




