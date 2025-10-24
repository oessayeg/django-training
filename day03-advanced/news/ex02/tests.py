from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from core.models import Article


class PublishViewTest(TestCase):
    def test_publish_view_with_anonymous_user(self):
        client = Client()
        response = client.get("/en/publish/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/en/login/?next=/en/publish/")

    def test_publish_view_with_authenticated_user(self):
        client = Client()
        User.objects.create_user(username="testuser", password="testpassword")
        client.login(username="testuser", password="testpassword")
        response = client.get("/en/publish/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ex02/publish.html")


class RegistrationViewTest(TestCase):
    def test_registration_view_with_anonymous_user(self):
        client = Client()
        response = client.get("/en/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ex02/registration.html")

    def test_registration_view_with_authenticated_user(self):
        client = Client()
        User.objects.create_user(username="testuser", password="testpassword")
        client.login(username="testuser", password="testpassword")
        response = client.get("/en/register/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/en/publications/")


class AddToFavoriteViewTest(TestCase):
    def test_add_to_favorite_view_with_authenticated_user(self):
        client = Client()

        User.objects.create_user(username="testuser", password="testpassword")
        Article.objects.create(
            title="Test Article",
            content="Test Content",
            author=User.objects.get(username="testuser"),
        )
        client.login(username="testuser", password="testpassword")
        add_to_favorite_first_response = client.post(
            "/en/add-to-favorite/1/", data={"article": 1}
        )
        add_to_favorite_second_response = client.post(
            "/en/add-to-favorite/1/", data={"article": 1}
        )

        self.assertEqual(add_to_favorite_first_response.status_code, 302)
        self.assertRedirects(add_to_favorite_first_response, "/en/publications/")

        self.assertEqual(add_to_favorite_second_response.status_code, 302)
        self.assertRedirects(add_to_favorite_second_response, "/en/publications/1/detail/")
        
        messages = list(get_messages(add_to_favorite_second_response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "This article is already in your favorites.")
        self.assertEqual(messages[0].level_tag, "warning")
