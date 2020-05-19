import json
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from .models import *
from .serializers import *
from tracker.permissions import *
from rest_framework.permissions import IsAuthenticated
import requests
from django.http import HttpRequest

from django.contrib.auth import login
from rest_framework import permissions
from knox.views import LoginView as KnoxLoginView


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
   # permission_classes = [IsAuthenticated, HasProjectPermission]

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, HasIssuePermission]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = IssueUpdateSerializer
        return serializer_class

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, HasCommentPermission]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated, ]


#############################################################

class AuthView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, code, format=None):
        class Auth:
            def __init__(self, code):
                self.client_id = '0ODR6pyyZcggO7YYkFHGssujPTaRPAKSuZCiCCln'
                self.client_secret = '8e6QtbeqpTo7xFrqcvZuVB61fQ6EZOGHEbEqLyGfT4grDoMZLND7X4Yj1Vp8J662Vd4q2o2TyPCgTPMqPEn2T1YGq9PHotswVJZJGa8Ayvu18L5kjpEGqVG36LBrpRfL'
                self.grant_type = 'authorization_code'
                self.redirect_url = 'http://localhost:3000/auth/'
                self.code = code
        auth_object = Auth(code)
        serializer = AuthSerializer(auth_object)
        token_response = requests.post('https://internet.channeli.in/open_auth/token/', data=serializer.data)
        if token_response.status_code == 200:
            login_response = requests.post('http://127.0.0.1:8000/tracker/api-auth/login/', data = token_response.json())
            return Response(login_response.json())
        return Response(token_response.json())

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):

        AUTH_TOKEN = 'Bearer '+request.data['access_token']
        headers = {'Authorization': AUTH_TOKEN}
        url = 'https://internet.channeli.in/open_auth/get_user_data/'
        data_response = requests.get(url, headers=headers)

        if data_response.status_code == 200:
            data_response = data_response.json()
            userId =  data_response['userId']
            name = (data_response['person']['fullName']).strip()
            email = data_response['contactInformation']['emailAddress']
            phoneNumber = data_response['contactInformation']['primaryPhoneNumber']
            try:
                username = name[:name.index(' ')]+'_'+str(userId)
            except ValueError:
                username = name+'_'+str(userId)
            try:
                requestUser = User.objects.get(userId = userId)
                serializer = AuthTokenSerializer(data={'userId': requestUser.userId})
                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data['user']
                login(request, user)
                return super(LoginView, self).post(request, format=None)
                

            except User.DoesNotExist:
                requestUser = User(userId = userId,
                    name = name,
                    email = email,
                    username = username,
                    phoneNumber = phoneNumber,
                    )
                requestUser.save()
                serializer = AuthTokenSerializer(data={'userId': requestUser.userId})
                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data['user']
                login(request, user)
                return super(LoginView, self).post(request, format=None)
        else:
            return Response(data_response.json())