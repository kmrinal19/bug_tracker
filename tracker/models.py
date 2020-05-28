from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField

class User(AbstractUser):
    first_name = None
    last_name = None
    password = None
    userId = models.BigIntegerField(unique = True)
    name = models.CharField(max_length = 180)
    phoneNumber = models.CharField(max_length = 15, blank = True)
    enrollmentNumber = models.CharField(max_length = 10, blank = True)

    USERNAME_FIELD = 'userId'
    required_fields = ['name','userId']

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length = 60, unique = True)
    wiki = RichTextUploadingField(null = True, blank = True)
    created_on = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User, on_delete = models.SET_NULL, related_name = 'created', null = True)
    team_member = models.ManyToManyField(User, related_name = 'teamMember_of', blank  = True)
    subscriber = models.ManyToManyField(User, related_name = 'projectSubscriber', blank = True)

    def __str__(self):
        return self.name

    def created_by_name(self):
        if(self.created_by):
            return self.created_by.name

    def team_member_name(self):
        return (list(map(lambda x: x.name, self.team_member.all())))

    def subscriber_name(self):
        return (list(map(lambda x: x.name, self.subscriber.all())))

class Tag(models.Model):
    tag_name = models.CharField(max_length = 20)

    def __str__(self):
            return self.tag_name

class Issue(models.Model):
    OPEN = 'O'
    CLOSED = 'C'
    status_choices = [(OPEN,'Open'),(CLOSED,'Close')]
    heading = models.TextField()
    description = RichTextUploadingField(null = True, blank = True)
    created_on = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User, on_delete = models.SET_NULL, related_name = 'issue_created', null = True)
    last_updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length = 1,choices = status_choices, default = OPEN)
    assigned_to = models.ManyToManyField(User, blank = True, related_name = 'assigned_issue')
    subscriber = models.ManyToManyField(User, related_name = 'issueSubscriber', blank = True)
    project = models.ForeignKey(Project, on_delete = models.CASCADE, related_name = 'projectIssues')
    issue_type = models.CharField(max_length = 20, default = 'bug')
    tag = models.ManyToManyField(Tag, related_name = 'tagIssues', blank = True)

    def __str__(self):
            return self.heading

    def created_by_name(self):
        if(self.created_by):
            return self.created_by.name

    def assigned_to_name(self):
        return (list(map(lambda x: x.name, self.assigned_to.all())))

    def subscriber_name(self):
        return (list(map(lambda x: x.name, self.subscriber.all())))

    def project_name(self):
        return self.project.name

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'comments', null = True)
    commentBody = RichTextUploadingField()
    commented_on = models.DateTimeField(auto_now = True)
    issue = models.ForeignKey(Issue, on_delete = models.CASCADE, related_name = 'issueComments')

    def user_name(self):
        return self.user.name

class Media(models.Model):
    media = models.ImageField(upload_to = 'upload_images')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null = True, related_name='project_media')
