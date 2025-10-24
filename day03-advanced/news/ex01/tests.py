from django.test import Client, TestCase
from django.contrib.auth.models import User


class PublicationsViewTest(TestCase):
    def test_publications_view_with_anonymous_user(self):
        client = Client()
        response = client.get("/en/publications/")
        self.assertEqual(response.status_code, 403)

    def test_publications_view_with_authenticated_user(self):
        client = Client()
        User.objects.create_user(username="testuser", password="testpassword")
        client.login(username="testuser", password="testpassword")
        response = client.get("/en/publications/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ex01/publications.html")


class FavoriteArticlesViewTest(TestCase):
    def test_favorite_articles_view_with_anonymous_user(self):
        client = Client()
        response = client.get("/en/favorite-articles/")
        self.assertEqual(response.status_code, 403)

    def test_favorite_articles_view_with_authenticated_user(self):
        client = Client()
        User.objects.create_user(username="testuser", password="testpassword")
        client.login(username="testuser", password="testpassword")
        response = client.get("/en/favorite-articles/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ex01/favourite_articles.html")
