from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework import routers

from posts.views import PostViewSet, GroupViewSet, CommentViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('posts', PostViewSet)
router_v1.register('groups', GroupViewSet)
router_v1.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]
