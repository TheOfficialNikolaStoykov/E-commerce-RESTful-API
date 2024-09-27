from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (OpenApiResponse, extend_schema,
                                   extend_schema_view)
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from users_app.signals import *

from .serializers import *


@extend_schema(
    request=ProfileRegistrationSerializer,
    responses={
        201: OpenApiResponse(description="Registration Successful with profile details"),
        400: OpenApiResponse(description="Bad Request")
    },
    description="Register a new user with profile details and obtain a token."
)
@api_view(["POST"])
def registration_view(request):
    serializer = ProfileRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        profile = get_object_or_404(Profile, user=user)

        data = {
            "response": "Registration Successful!",
            "username": user.username,
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "phone_number": str(profile.phone_number),
            "address_line_1": profile.address_line_1,
            "address_line_2": profile.address_line_2,
            "city": profile.city,
            "state": profile.state,
            "postal_code": profile.postal_code,
            "country": profile.country,
            "token": Token.objects.get(user=user).key,
        }
        return Response(data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    description="Log out the current user by deleting their auth token.",
    responses={
        200: OpenApiResponse(response=None, description="Token deleted successfully"),
        400: OpenApiResponse(response=None, description="Bad Request"),
    }
)
@api_view(["POST"])
def logout_view(request):
    """
    Log out the current user.
    """
    try:
        request.user.auth_token.delete()
        return Response({"message": "Token deleted successfully"}, status=status.HTTP_200_OK)
    except Exception:
        return Response({"error": "Could not delete token"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    get=extend_schema(
        description="List all user profiles. Accessible only to admin users.",
        responses={200: ProfileViewSerializer(many=True)}
    )
)
@api_view(["GET"])
@permission_classes([IsAdminUser])
def list_profiles_view(request):
    """
    List all user profiles. Admin only.
    """
    profiles = Profile.objects.all()
        
    serializer = ProfileViewSerializer(profiles, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    description="Retrieve a single user profile by ID.",
    responses={200: ProfileUpdateSerializer}
)
@api_view(["GET"])
def retrieve_single_profile_view(request, pk):
    """
    Retrieve a single user profile by ID.
    """
    profile = get_object_or_404(Profile, pk=pk)
        
    serializer = ProfileUpdateSerializer(profile)
    return Response(serializer.data)


@extend_schema_view(
    put=extend_schema(
        description="Update a user profile using PUT. Admin only.",
        request=ProfileUpdateSerializer,
        responses={200: ProfileUpdateSerializer}
    ),
    patch=extend_schema(
        description="Partially update a user profile using PATCH. Admin only.",
        request=ProfileUpdateSerializer,
        responses={200: ProfileUpdateSerializer}
    )
)
@api_view(["PUT", "PATCH"])
@permission_classes([IsAdminUser])
def edit_profile_view(request, pk):
    """
    Edit a user profile (PUT or PATCH). Admin only.
    """
    profile = get_object_or_404(Profile, pk=pk)

    if request.method == "PUT":
        serializer = ProfileUpdateSerializer(profile, data=request.data)
    else:
        serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    description="Delete a user profile by ID. Admin only.",
    responses={204: None}
)
@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_profile_view(request, pk):
    """
    Delete a user profile. Admin only.
    """
    profile = get_object_or_404(Profile, pk=pk)
    profile.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)