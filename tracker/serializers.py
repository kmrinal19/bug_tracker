from tracker.models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'heading', 'description',
            'created_by', 'created_on', 'assigned', 
            'subscriber', 'project', 'last_updated',
            'status', 'tag_set', 'issueComments',
            'issue_type']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'wiki', 
            'created_on', 'created_by', 
            'team_member', 'subscriber', 
            'projectIssues']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'commentBody', 'commented_on',
            'issue']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name',
            'last_name', 'email', 'date_joined',
            'is_superuser', 'is_staff', 'is_active', 
            'last_login', 'teamMember_of', 'issue_created',
            'issue_assigned', 'comments']