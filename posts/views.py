from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .serializers import PostSerializer

from api.views import AuthTokenView


class PostViewSet(AuthTokenView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
