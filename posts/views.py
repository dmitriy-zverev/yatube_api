from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer

from api.permissions import IsAuthorOrReadOnly, IsAuthenticatedCustom
from api.views import AuthTokenView


class PostViewSet(AuthTokenView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedCustom]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(AuthTokenView):
    http_method_names = ['get', 'head', 'options']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(AuthTokenView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedCustom]

    def get_queryset(self):
        post_id = self.kwargs['post_pk']
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_pk']
        serializer.save(post_id=post_id, author=self.request.user)
