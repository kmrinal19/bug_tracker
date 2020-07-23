from tracker.models import *
from rest_framework import serializers
from django.core.mail import send_mail
from bug_tracker.settings import EMAIL_HOST_USER


class ProjectMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMedia
        fields = '__all__'

class IssueMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueMedia
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField()

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user']

class IssueSerializer(serializers.ModelSerializer):
    issue_media = IssueMediaSerializer(many = True, read_only = True)
    issueComments = CommentSerializer(many = True, read_only = True)
    created_by_name = serializers.ReadOnlyField()
    assigned_to_name = serializers.ReadOnlyField()
    subscriber_name = serializers.ReadOnlyField()
    project_name = serializers.ReadOnlyField()
    tag_name = serializers.ReadOnlyField()

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        team_member_list = validated_data['project'].team_member.all()
        project = validated_data['project']
        email_list = list(map(lambda x: x.email,team_member_list))
        send_mail(
            'New Issue Reported',
            self.context['request'].user.name+' reported a new issue in project : '+project.name,
            EMAIL_HOST_USER,
            email_list,
            fail_silently=False
        )
        if self.context['request'].user in team_member_list or self.context['request'].user.is_superuser:
            pass
        else:
            validated_data.pop('assigned_to', None)

        images_data = self.context.get('view').request.FILES

        if images_data:
            issue = Issue.objects.create(
                heading = validated_data['heading'],
                description = validated_data['description'],
                created_by = validated_data['created_by'],
                project = validated_data['project'],
                issue_type = validated_data['issue_type']
            )
            for image_data in images_data.values():
                IssueMedia.objects.create(issue = issue, media = image_data)

            return issue

        return super().create(validated_data)

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['subscriber', 'created_by']

class IssueUpdateSerializer(serializers.ModelSerializer):
    issueComments = CommentSerializer(many = True, read_only = True)  
    assigned_to_name = serializers.ReadOnlyField()
    tag_name = serializers.ReadOnlyField()

    def update(self, instance, validated_data):
        team_members_list = instance.project.team_member.all()
        if self.context['request'].user in team_members_list or self.context['request'].user.is_superuser:
            return super().update(instance, validated_data)
        else:
            validated_data.pop('assigned_to', None)
            return super().update(instance, validated_data)
    
    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['heading', 'description', 'created_by', 'project', 'subscriber']

class ProjectSerializer(serializers.ModelSerializer):
    project_media = ProjectMediaSerializer(many = True, read_only = True)
    projectIssues = IssueSerializer(many = True, read_only = True)
    created_by_name = serializers.ReadOnlyField()
    team_member_name = serializers.ReadOnlyField()
    subscriber_name = serializers.ReadOnlyField()

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        admins_email = list(map(lambda x: x.email, User.objects.filter(is_superuser = True))) 

        send_mail(
        'New Project created',
        self.context['request'].user.name+' created a new project : '+validated_data['name'],
        EMAIL_HOST_USER,
        admins_email,
        fail_silently=False
    )

        if self.context['request'].user not in validated_data['team_member']:
            validated_data['team_member'].append(self.context['request'].user)

        images_data = self.context.get('view').request.FILES

        if images_data:
            project = Project.objects.create(
                name = validated_data['name'],
                wiki = validated_data['wiki'],
                created_by = validated_data['created_by'],
            )
            project.team_member.set(validated_data['team_member'])
            for image_data in images_data.values():
                ProjectMedia.objects.create(project = project, media = image_data)

            return project

        return super().create(validated_data)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['subscriber', 'created_by']

class ProjectUpdateSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):

        images_data = self.context.get('view').request.FILES

        if images_data:
            for image_data in images_data.values():
                ProjectMedia.objects.create(project = instance, media = image_data)

        return super().update(instance, validated_data)

    class Meta:
        model = Project
        fields = ['wiki','team_member','id']

class UserSerializer(serializers.ModelSerializer):
    teamMember_of_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'name','phoneNumber','username',
            'email', 'date_joined', 'enrollmentNumber',
            'is_superuser', 'is_staff', 'is_active', 
            'last_login', 'teamMember_of', 'issue_created',
            'assigned_issue', 'comments', 'issueSubscriber',
            'projectSubscriber', 'created','userId',
            'teamMember_of_name', 'issue_created_name', 'assigned_issue_name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class AuthSerializer(serializers.Serializer):
    client_id = serializers.CharField(required = True)
    client_secret = serializers.CharField(required = True)
    grant_type = serializers.CharField(required = True)
    redirect_url = serializers.CharField(required = True)
    code = serializers.CharField(required = True)

#######################################################################

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class AuthTokenSerializer(serializers.Serializer):
    userId = serializers.CharField(
        label=_("userId"),
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        userId = attrs.get('userId')

        if userId:
            user = authenticate(request=self.context.get('request'),
                                userId = userId)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username"')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs