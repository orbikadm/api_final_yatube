from rest_framework.viewsets import *
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Post, Follow, Group, Comment
from .serializers import PostSerializer, FollowSerializer, GroupSerializer, CommentSerializer
from .permissions import IsOwnerOnly, ReadOnly, OwnerOrReadOnly

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions() 


class FollowViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions() 


class CommentsViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs.get('post_id'))
    
    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.id,
            post=self.kwargs.get('post_id')
        )

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions() 