from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CommentsViewSet, FollowViewSet, GroupViewSet, PostViewSet
from posts.models import Follow

v1_router = DefaultRouter()
v1_router.register('posts', PostViewSet)
v1_router.register('follow', FollowViewSet, Follow.objects.all())
v1_router.register('groups', GroupViewSet)
v1_router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentsViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(v1_router.urls)),
]
