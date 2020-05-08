from tracker.models import *
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'commentBody', 'commented_on',
            'issue']

class IssueSerializer(serializers.ModelSerializer):
    issueComments = CommentSerializer(many = True, read_only = True)
    class Meta:
        model = Issue
        fields = ['id', 'heading', 'description',
            'created_by', 'created_on', 'assigned_to', 
            'subscriber', 'project', 'last_updated',
            'status', 'tag', 'issueComments',
            'issue_type']

class ProjectSerializer(serializers.ModelSerializer):
    projectIssues = IssueSerializer(many = True, read_only = True)
    class Meta:
        model = Project
        fields = ['id', 'name', 'wiki', 
            'created_on', 'created_by', 
            'team_member', 'subscriber', 
            'projectIssues']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name',
            'last_name', 'email', 'date_joined',
            'is_superuser', 'is_staff', 'is_active', 
            'last_login', 'teamMember_of', 'issue_created',
            'issue_assigned', 'comments']