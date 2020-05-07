from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

admin.site.register(User, UserAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(IssueAssignment)