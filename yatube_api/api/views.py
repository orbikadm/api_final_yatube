from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter

from posts.models import Post, Follow, Group, Comment
from .serializers import (
    CommentSerializer, GroupSerializer, FollowSerializer, PostSerializer
)
from .permissions import OwnerOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (OwnerOrReadOnly,)


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly,)

    def get_queryset(self):
        # post = Post.objects.get(self.kwargs.get('post_id'))
        # return post.comments
        return Comment.objects.filter(post=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        serializer.save(
            author_id=self.request.user.id,
            post_id=self.kwargs.get('post_id')
        )
