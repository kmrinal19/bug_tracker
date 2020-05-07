from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tracker import views

router = DefaultRouter()
router.register(r'project', views.ProjectViewSet)
router.register(r'issue', views.IssueViewSet)
router.register(r'comment', views.CommentViewSet)
router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]