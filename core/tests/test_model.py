from rest_framework.test import APITestCase
from core.models import User, Investor, Feedback, Poi, Document
from .test_setup import TestSetUp


class TestModel(TestSetUp):
    def test_creates_user(self):
        user = User.objects.create_user(
            username="username",
            email="email@test.com",
            phone="08156912547",
            password="password1@212",
        )
        self.assertEqual(user.username, "username")
        self.assertFalse(user.is_staff)

    def test_creates_super_user(self):
        user = User.objects.create_superuser(
            username="username",
            email="email@test.com",
            password="password1@212",
        )
        self.assertEqual(user.username, "username")
        self.assertTrue(user.is_staff)

    def test_cant_create_user_without_username(self):
        self.assertRaises(
            ValueError,
            User.objects.create_user,
            email=self.user_data["email"],
            password=self.user_data["password"],
            phone=self.user_data["phone"],
            username="",
        )

        with self.assertRaisesMessage(ValueError, "Users must have a username"):
            User.objects.create_user(
                email=self.user_data["email"],
                phone=self.user_data["phone"],
                password=self.user_data["password"],
                username="",
            )

    def test_cant_create_user_without_email(self):
        self.assertRaises(
            ValueError,
            User.objects.create_user,
            email="",
            password=self.user_data["password"],
            phone=self.user_data["phone"],
            username=self.user_data["username"],
        )

        with self.assertRaisesMessage(ValueError, "Users must have an email address"):
            User.objects.create_user(
                email="",
                phone=self.user_data["phone"],
                password=self.user_data["password"],
                username=self.user_data["username"],
            )

    def test_cant_create_user_without_phone(self):
        self.assertRaises(
            ValueError,
            User.objects.create_user,
            email=self.user_data["email"],
            password=self.user_data["password"],
            phone="",
            username=self.user_data["username"],
        )

        with self.assertRaisesMessage(ValueError, "Users must have a phone"):
            User.objects.create_user(
                email=self.user_data["email"],
                phone="",
                password=self.user_data["password"],
                username=self.user_data["username"],
            )

    def test_creates_feedback(self):
        user = User.objects.create_user(
            username="username",
            email="email@test.com",
            phone="08156912547",
            password="password1@212",
        )
        feedback = Feedback.objects.create(
            user=user, title="Feedback title", text="Feedback body"
        )
        self.assertIsInstance(feedback, Feedback)
        self.assertEqual(feedback.title, "Feedback title")

    def test_creates_investor(self):
        user = User.objects.create_user(
            username="username",
            email="email@test.com",
            phone="08156912547",
            password="password1@212",
        )
        investor = Investor.objects.create(user=user, name="Investor")
        self.assertIsInstance(investor, Investor)
        self.assertEqual(investor.name, "Investor")

    def test_creates_poi(self):
        user = User.objects.create_user(
            username="username",
            email="email@test.com",
            phone="08156912547",
            password="password1@212",
        )
        poi = Poi.objects.create(user=user, id_type="BVN", content="444444444")
        self.assertIsInstance(poi, Poi)
        self.assertEqual(poi.id_type, "BVN")

    def test_creates_document(self):
        user = User.objects.create_user(
            username="username",
            email="email@test.com",
            phone="08156912547",
            password="password1@212",
        )
        document = Document.objects.create(user=user, doc_type="Passport")
        self.assertIsInstance(document, Document)
        self.assertEqual(document.doc_type, "BVN")
