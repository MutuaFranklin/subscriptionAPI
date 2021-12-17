from .serializer import UserSerializer, ProfileSerializer,ContentSerializer ,PlanSerializer, TransactionSerializer
from .models import Profile, Content
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.http.response import JsonResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.parsers import JSONParser
from django.conf import settings
from djangoflutterwave.models import FlwPlanModel,FlwTransactionModel
from django.db.models import Q
import requests
import math
import random


class UserViewSet(viewsets.ModelViewSet):
    """
    view or edit users.
    """
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def profile(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()

    if request.method == 'GET':
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        profile_serializer = ProfileSerializer(instance=profile, data=request.data,context={'request': request})

        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((IsAuthenticated,))
def content(request):
    user = request.user
    current_user_profile = Profile.objects.filter(user=user).first()
    premium_profiles = Profile.objects.filter(access_plan =1)
    all_content = Content.objects.all()
    free_content =Content.objects.filter(~Q(content_accessplan=1))




    if request.method == 'GET':
            if current_user_profile in premium_profiles:
                serializer = ContentSerializer(all_content, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                serializer = ContentSerializer(free_content, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            
    elif request.method == 'POST':
        content_serializer = ContentSerializer(instance=all_content, data=request.data,context={'request': request})

        if content_serializer.is_valid():
            content_serializer.save()
            return Response(content_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(content_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


