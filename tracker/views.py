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

class AuthView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, code, format=None):
        class Auth:
            def __init__(self, code):
                self.client_id = 'cCeEneHzwStHFliDuSWrPLIsH334e0wppnK8ViHL'
                self.client_secret = 'OTDFf6g8S2I1VDTSjEWbcsGTJfhTFI23BSMm2ZfyoH0Ov1vcwQv6CrDcwUhj6ByQmVTW0VVxKdZ4hTUAvwBedSiMXXS7uGPE56oxKgyApfLP0G3HrNLaHExLNpTQQZZN'
                self.grant_type = 'authorization_code'
                self.redirect_url = 'http://localhost:3000/auth/'
                self.code = code
        auth_object = Auth(code)
        serializer = AuthSerializer(auth_object)
        token_response = requests.post('https://internet.channeli.in/open_auth/token/', data=serializer.data)
        if token_response.status_code == 200:
            AUTH_TOKEN = 'Bearer '+token_response.json()['access_token']
            headers = {'Authorization': AUTH_TOKEN}
            url = 'https://internet.channeli.in/open_auth/get_user_data/'
            data_response = requests.get(url, headers=headers)

            if data_response.status_code == 200:
                # return Response(data_response.json())
                data_response = data_response.json()
                user_object = {
                    'userId': data_response['userId'],
                    'name': data_response['person']['fullName'],
                    'email': data_response['contactInformation']['emailAddress'],
                    'phoneNumber': data_response['contactInformation']['primaryPhoneNumber']
                }
                return Response(json.dumps(user_object))

            else:
                return Response(data_response.json())
        return Response(token_response.json())

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)