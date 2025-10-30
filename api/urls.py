from django.urls import include, path
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from rest_framework.authtoken.views import obtain_auth_token

from posts.views import PostViewSet, GroupViewSet, CommentViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('posts', PostViewSet)
router_v1.register('groups', GroupViewSet)

posts_router = nested_routers.NestedDefaultRouter(router_v1,
                                                  r'posts',
                                                  lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include(posts_router.urls)),
    path('api-token-auth/', obtain_auth_token),
]
