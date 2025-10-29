from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework import routers

from posts.views import PostViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('posts', PostViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]
