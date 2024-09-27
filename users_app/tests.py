from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users_app.models import *


class UserTestCase(APITestCase):
    """
    Test case for user-related actions, including login, registration, logout, and profile management.
    """

    def setUp(self):
        """
        Set up test data, including an admin user, a regular user, and associated profiles.
        """
        self.admin_user = User.objects.create_superuser(username="test_admin_user", password="password")
        self.user = User.objects.create_user(username="test_user", password="password", email="example@example.com")
        self.user_profile = Profile.objects.create(
            user=self.user,
            first_name="Test",
            last_name="User",
            phone_number="+11234567890",
            address_line_1="Test Address 1",
            address_line_2="Test Address 2",
            city="Test City",
            postal_code=1999,
            state="Test State",
            country="Test Country"
        )
        self.admin_profile = Profile.objects.create(
            user=self.admin_user,
            first_name="Admin",
            last_name="User",
            phone_number="+11234567891",
            address_line_1="Admin Address 1",
            address_line_2="Admin Address 2",
            city="Admin City",
            postal_code=2000,
            state="Admin State",
            country="Admin Country"
        )

    def test_login(self):
        """
        Test login functionality with valid user credentials.
        """
        data = {
            "username": self.user.username,
            "password": "password"
        }
        
        response = self.client.post(reverse("login"), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_register_200(self):
        """
        Test user registration with valid data.
        """
        data = {
            "username": "new_username",
            "password": "new_password",
            "email": "new_user@example.com",
            "first_name": "New",
            "last_name": "User",
            "phone_number": "+14155552671",
            "address_line_1": "New Address 1",
            "address_line_2": "New Address 2",
            "city": "New City",
            "postal_code": 1234,
            "state": "Sofia",
            "country": "Bulgaria"
        }
        
        response = self.client.post(reverse("register"), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_register_duplicate_usernames(self):
        """
        Test registration with a duplicate username.
        """
        data = {
            "username": self.user.username,
            "password": "new_password",
            "email": "new_user@example.com",
            "first_name": "New",
            "last_name": "User",
            "phone_number": "+14155552671",
            "address_line_1": "New Address 1",
            "address_line_2": "New Address 2",
            "city": "New City",
            "postal_code": 1234,
            "state": "Sofia",
            "country": "Bulgaria"
        }
        
        response = self.client.post(reverse("register"), data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_duplicate_emails(self):
        """
        Test registration with a duplicate email.
        """
        data = {
            "username": "new_user",
            "password": "new_password",
            "email": self.user.email,
            "first_name": "New",
            "last_name": "User",
            "phone_number": "+14155552671",
            "address_line_1": "New Address 1",
            "address_line_2": "New Address 2",
            "city": "New City",
            "postal_code": 1234,
            "state": "Sofia",
            "country": "Bulgaria"
        }
        
        response = self.client.post(reverse("register"), data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_400(self):
        """
        Test registration with missing required fields.
        """
        data = {
            "username": "",
            "password": "",
        }
        
        response = self.client.post(reverse("register"), data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_invalid_email_format(self):
        """
        Test registration with an invalid email format.
        """
        data = {
            "username": "new_user",
            "password": "password123",
            "email": "invalid_email",
            "first_name": "New",
            "last_name": "User",
            "phone_number": "+14155552671",
            "address_line_1": "New Address 1",
            "address_line_2": "New Address 2",
            "city": "New City",
            "postal_code": 1234,
            "state": "Sofia",
            "country": "Bulgaria"
        }
        
        response = self.client.post(reverse("register"), data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout(self):
        """
        Test logging out a user and invalidating the token.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        
        data = {
            "username": self.user.username,
            "password": "password"
        }

        response = self.client.post(reverse("logout"), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_logout_token_deletion_failure(self):
        """
        Test logout failure due to missing token.
        """
        self.client.login(username=self.user.username, password=self.user.password)

        Token.objects.filter(user=self.user).delete()

        response = self.client.post(reverse("logout"))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_profiles(self):
        """
        Test listing all user profiles (admin-only).
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)
 
        response = self.client.get(reverse("profiles"))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_profile(self):
        """
        Test retrieving a single profile by its ID (admin-only).
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.get(reverse("profile", args=(self.user_profile.id,)))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_single_profile_put(self):
        """
        Test editing a profile using PUT (admin-only).
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "username": self.user.username,
            "password": self.user.password,
            "email": "valid_email@example.com",
            "first_name": "ValidName",
            "last_name": "UpdatedLastName",
            "phone_number": "+14155552671",
            "address_line_1": "Updated Address 1",
            "address_line_2": "Updated Address 2",
            "city": "ValidCity",
            "state": "ValidState",
            "postal_code": 4321,
            "country": "ValidCntry"
        }

        response = self.client.put(reverse("profile-edit", args=(self.user_profile.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_edit_single_profile_put_400(self):
        """
        Test editing a profile with invalid data using PUT (admin-only).
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)
        
        invalid_data = {
            "first_name": "",
            "last_name": ""
        }
        
        response = self.client.put(reverse("profile-edit", args=(self.user_profile.id,)), invalid_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_single_profile_patch(self):
        """
        Test editing a profile using PATCH (admin-only).
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "username": self.user.username,
            "password": self.user.password,
            "phone_number": "+14155552671",
            "first_name": "Test Name",
            "email": "example@example.com"
        }
        
        response = self.client.patch(reverse("profile-edit", args=(self.user_profile.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_single_profile(self):
        """
        Test deleting a profile (admin-only).
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)
        
        response = self.client.delete(reverse("profile-delete", args=(self.user_profile.id,)))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)