from rest_framework import permissions

class HasProjectPermission(permissions.BasePermission):

    """
    Custom permissions to allow only team members and admins to edit the project
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser or request.user in obj.team_member.all():
            return True
        
        return False

class HasIssuePermission(permissions.BasePermission):

    """
    Custom permissions to allow only issue creator, team members and admins to edit the issue
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user == obj.created_by:
            if request.method == 'DELETE':
                return True

        if (request.user.is_superuser) or (request.user in obj.project.team_member.all()):
            return True

        return False

class HasCommentPermission(permissions.BasePermission):

    """
    Custom permissions to allow only comment author, team members and admins to edit the comment
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if (request.user.is_superuser) or (request.user == obj.user) or (request.user in obj.issue.project.team_member.all()):
            return True

        return False