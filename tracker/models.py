from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class User(AbstractUser):
    pass

class Project(models.Model):
    name = models.CharField(max_length = 60, unique = True)
    wiki = RichTextUploadingField(null = True, blank = True)
    created_on = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User, on_delete = models.SET_NULL, related_name = 'created', null = True)
    team_member = models.ManyToManyField(User, related_name = 'teamMember_of')
    subscriber = models.ManyToManyField(User, related_name = 'projectSubscriber', blank = True)

    def __str__(self):
        return self.name

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
    assigned = models.ManyToManyField(User,through = 'IssueAssignment', through_fields = ('issue', 'assigned_to'), related_name = 'issue_assigned')
    subscriber = models.ManyToManyField(User, related_name = 'issueSubscriber', blank = True)
    project = models.ForeignKey(Project, on_delete = models.CASCADE, related_name = 'projectIssues')
    issue_type = models.CharField(max_length = 20, default = 'bug')

    def __str__(self):
            return self.heading

class IssueAssignment(models.Model):
    assigned_to = models.ForeignKey(User, on_delete = models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete = models.CASCADE)
    assigned_by = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, related_name = 'issue_assigned_by')
    
    class Meta:
        unique_together = ('assigned_to', 'issue',)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'comments')
    commentBody = RichTextUploadingField()
    commented_on = models.DateTimeField(auto_now = True)
    issue = models.ForeignKey(Issue, on_delete = models.CASCADE, related_name = 'issueComments')

class Tag(models.Model):
    issue = models.ForeignKey(Issue, on_delete = models.CASCADE)
    tag = models.CharField(max_length = 20)

    def __str__(self):
            return self.tag

    class Meta:
        unique_together = ('issue', 'tag',)