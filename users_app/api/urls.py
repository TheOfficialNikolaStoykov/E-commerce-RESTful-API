from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import *

urlpatterns = [
    path("login/", obtain_auth_token, name="login"),
    path("register/", registration_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("view/all/", list_profiles_view, name="profiles"),
    path("view/<int:pk>/", retrieve_single_profile_view, name="profile"),
    path("edit/<int:pk>/", edit_profile_view, name="profile-edit"),
    path("delete/<int:pk>/", delete_profile_view, name="profile-delete")
]