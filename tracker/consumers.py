import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from knox.auth import TokenAuthentication
from rest_framework import exceptions, HTTP_HEADER_ENCODING

from django.core.mail import send_mail

from tracker.models import Issue, Comment
from tracker.serializers import CommentSerializer
from bug_tracker.settings import EMAIL_HOST_USER

class ChatConsumer(WebsocketConsumer):
    def connect(self):

        self.token = self.scope['url_route']['kwargs']['token']
        self.issueID = self.scope['url_route']['kwargs']['issueID']
        self.room_group_name = 'issue_'+str(self.issueID)

        knoxAuth = TokenAuthentication()
        user, auth_token = knoxAuth.authenticate_credentials(self.token.encode(HTTP_HEADER_ENCODING))

        if user:

            try:
                self.issue = Issue.objects.get(id = self.issueID)
                self.user = user
                async_to_sync(self.channel_layer.group_add)(
                    self.room_group_name,
                    self.channel_name
                )       
                self.accept()

            except Issue.DoesNotExist:
                pass

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        comment = self.issue.issueComments.create(user = self.user, commentBody = message)
        serializer = CommentSerializer(comment)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': json.dumps(serializer.data)
            }
        )

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=message)
        send_mail(
            'New Comment on Issue: '+self.issue.heading,
            self.user.name+' commented on your issue: '+self.issue.heading,
            EMAIL_HOST_USER,
            [self.issue.created_by.email],
            fail_silently=False
        )