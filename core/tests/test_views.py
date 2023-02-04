from .test_setup import TestSetUp
from core.models import User, Investor, Feedback, Poi, Document
from rest_framework import status
from django.urls import reverse
from http.cookies import SimpleCookie


class TestViews(TestSetUp):
    def authenticate(self):

        self.client.cookies = SimpleCookie({"csrftoken": "token"})
        response = self.client.post(self.register_url, self.user_data, format="json")
        email = response.data["email"]
        user = User.objects.get(email=email)
        user.is_verified = True
        user.save()
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {res.data['tokens']['access']}"
        )
        return user

    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register_correctly(self):
        res = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(res.data["email"], self.user_data["email"])
        self.assertEqual(res.data["username"], self.user_data["username"])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_login_after_verification(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        email = response.data["email"]
        user = User.objects.get(email=email)
        user.is_verified = True
        user.save()
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_gives_descriptive_errors_on_register(self):
        response = self.client.post(
            self.register_url, {"email": self.user_data["email"]}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        user = self.verified_user()
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data["tokens"]["access"], str)

    def test_gives_descriptive_errors_on_login(self):
        response = self.client.post(
            self.login_url,
            {"email": "test@site.com", "password": self.user_data["password"]},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_resets_user_password(self):
        user = self.verified_user()
        response = self.client.post(
            reverse("reset-password"),
            {
                "email": user.email,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_sets_new_password(self):
    #     user = self.verified_user()
    #     data = {"email": user.email, "password": "new-password"}
    #     response = self.client.patch(reverse("set-new-password"), data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_gives_descriptive_errors_on_reset_password(self):
        response = self.client.post(
            reverse("reset-password"),
            {"email": "test@site.com"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_sets_new_password_without_otp(self):
        user = self.verified_user()
        data = {"email": user.email, "password": "new-password"}
        response = self.client.patch(reverse("set-new-password"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_investor(self):
        self.authenticate()
        ## create investor
        data = {
            "name": "Investor Name",
            "professional_status": "prof",
            "professional_cat": "Cat",
            "professional_subcat": "sub-cat",
            "income": "average",
            "experience": "Expert",
        }
        self.create_investor_res = self.client.post(
            reverse("investor-create"), data, format="json"
        )
        self.assertEqual(self.create_investor_res.status_code, status.HTTP_201_CREATED)
        return self.create_investor_res.data

    # def test_retrieve_investor(self):

    #     user = self.authenticate()
    #     ## investor-detail
    #     inv = Investor.objects.create(user=user, name="Investor")

    #     res = self.client.get(reverse("investor-detail", kwargs={"slug": inv.slug}))
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_update_investor(self):
    #     pass

    # def test_delete_investor(self):
    #     pass

    def test_get_users_followers(self):
        user = self.authenticate()
        res = self.client.get(reverse("user_followers", kwargs={"slug": user.slug}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_users_following(self):
        user = self.authenticate()
        res = self.client.get(reverse("user_following", kwargs={"slug": user.slug}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_follow_user(self):
        self.authenticate()
        utf = User.objects.create_user(
            email="example@email.com",
            username="example",
            phone="12345678901",
            password="password",
        )
        utf.is_verified = True
        utf.save()
        res = self.client.post(reverse("follow_user", kwargs={"slug": utf.slug}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_unfollow_user(self):
        self.authenticate()
        utu = User.objects.create_user(
            email="example@email.com",
            username="example",
            phone="12345678901",
            password="password",
        )
        utu.save()
        res = self.client.post(reverse("unfollow_user", kwargs={"slug": utu.slug}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_user(self):
        user = self.authenticate()
        res = self.client.get(reverse("user_profile", kwargs={"slug": user.slug}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_patch_user(self):
        user = self.authenticate()
        data = {"bio": "New Bio"}

        res = self.client.patch(
            reverse("user_profile", kwargs={"slug": user.slug}), data, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_destroy_user(self):
        user = self.authenticate()
        res = self.client.delete(reverse("user_profile", kwargs={"slug": user.slug}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_feedback(self):
        user = self.authenticate()
        data = {"title": "Feedback Title", "text": "Feedback Text"}
        res = self.client.post(reverse("feedback-create"), data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        return res.data

    def test_retrieve_feedback(self):
        user = self.authenticate()
        feed = Feedback.objects.create(
            user=user, title="Feedback Title", text="Feedback Text"
        )
        feed.save()
        res = self.client.get(reverse("feedback-detail", kwargs={"pk": feed.pk}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_feedback(self):
        user = self.authenticate()
        feed = Feedback.objects.create(
            user=user, title="Feedback Title", text="Feedback Text"
        )
        feed.save()
        data = {"title": "New Bio"}

        res = self.client.patch(
            reverse("feedback-update", kwargs={"pk": feed.pk}), data, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_delete_feedback(self):
        user = self.authenticate()
        feed = Feedback.objects.create(
            user=user, title="Feedback Title", text="Feedback Text"
        )
        feed.save()
        res = self.client.delete(reverse("feedback-delete", kwargs={"pk": feed.pk}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_poi(self):
        user = self.authenticate()
        data = {"id_type": "BVN", "content": "456734578"}
        res = self.client.post(reverse("poi-create"), data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        return res.data

    def test_create_document(self):
        user = self.authenticate()
        data = {"doc_type": "Passport"}
        res = self.client.post(reverse("document-create"), data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        return res.data
