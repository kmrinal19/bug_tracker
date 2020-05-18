from tracker.models import *
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user']

class IssueSerializer(serializers.ModelSerializer):
    issueComments = CommentSerializer(many = True, read_only = True)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        team_member_list = validated_data['project'].team_member.all()
        if self.context['request'].user in team_member_list or self.context['request'].user.is_superuser:
            return super().create(validated_data)
        else:
            validated_data.pop('assigned_to', None)
            return super().create(validated_data)

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['subscriber', 'created_by']

class IssueUpdateSerializer(serializers.ModelSerializer):
    issueComments = CommentSerializer(many = True, read_only = True)  

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
    projectIssues = IssueSerializer(many = True, read_only = True)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user

        if self.context['request'].user not in validated_data['team_member']:
            validated_data['team_member'].append(self.context['request'].user)

        return super().create(validated_data)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['subscriber', 'created_by']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'name','phoneNumber',
            'email', 'date_joined', 'enrollmentNumber',
            'is_superuser', 'is_staff', 'is_active', 
            'last_login', 'teamMember_of', 'issue_created',
            'assigned_issue', 'comments', 'issueSubscriber',
            'projectSubscriber', 'userId']

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
    username = serializers.CharField(
        label=_("Username"),
        write_only=True
    )
    # password = serializers.CharField(
    #     label=_("Password"),
    #     style={'input_type': 'password'},
    #     trim_whitespace=False,
    #     write_only=True
    # )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')

        if username:
            user = authenticate(request=self.context.get('request'),
                                username=username)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username"')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs