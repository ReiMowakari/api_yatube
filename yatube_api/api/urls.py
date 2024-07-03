from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, GroupViewSet, CommentViewSet


# Создаем объект роутера.
router_version_1 = DefaultRouter()

# Регистрируем маршруты постов.
router_version_1.register('posts', PostViewSet, basename='posts')

# Регистрируем маршруты групп.
router_version_1.register('groups', GroupViewSet, basename='groups')

# Регистрируем маршруты комментариев.
router_version_1.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router_version_1.urls)),
]
