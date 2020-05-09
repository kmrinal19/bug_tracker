from tracker.models import *
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class IssueSerializer(serializers.ModelSerializer):
    issueComments = CommentSerializer(many = True, read_only = True)
    class Meta:
        model = Issue
        fields = '__all__'

class IssueUpdateSerializer(serializers.ModelSerializer):
    issueComments = CommentSerializer(many = True, read_only = True)
    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['heading', 'description', 'created_by', 'project', ]

class ProjectSerializer(serializers.ModelSerializer):
    projectIssues = IssueSerializer(many = True, read_only = True)
    class Meta:
        model = Project
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name',
            'last_name', 'email', 'date_joined',
            'is_superuser', 'is_staff', 'is_active', 
            'last_login', 'teamMember_of', 'issue_created',
            'assigned_issue', 'comments']