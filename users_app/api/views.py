from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from users_app.signals import *

from .serializers import *


@api_view(["POST"])
def registration_view(request):
    serializer = ProfileRegistrationSerializer(data=request.data)
    
    data = {}

    if serializer.is_valid():
        user = serializer.save()

        profile = get_object_or_404(Profile, user=user)

        data["response"] = "Registration Successful!"
        data["username"] = user.username
        data["first_name"] = profile.first_name
        data["last_name"] = profile.last_name
        data["phone_number"] = profile.phone_number
        data["address_line_1"] = profile.address_line_1
        data["address_line_2"] = profile.address_line_2
        data["city"] = profile.city
        data["state"] = profile.state
        data["postal_code"] = profile.postal_code
        data["country"] = profile.country

        token = Token.objects.get(user=user).key
        data["token"] = token

    else:
        data = serializer.errors
    
    return Response(data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def logout_view(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)
    
@api_view(["GET"])
@permission_classes([IsAdminUser]) 
def list_profiles_view(request):
    profiles = Profile.objects.all()
        
    serializer = ProfileViewSerializer(profiles, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def retrieve_single_profile_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
        
    serializer = ProfileUpdateSerializer(profile)
    return Response(serializer.data)

@api_view(["PUT", "PATCH"])
@permission_classes([IsAdminUser])
def edit_profile_view(request, pk):
    if request.method == "PUT":
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileUpdateSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "PATCH":
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_profile_view(request, pk):  
    profile = get_object_or_404(Profile, pk=pk)
    profile.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)