from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from posts.models import Post, Group


class AuthorizedModelViewSet(ModelViewSet):
    """
    Базовый вьюсет, требующий авторизованного автора для изменения собственных данных.
    Вынес в отдельный вьюсет, основанный на ModelViewSet для того,
    чтобы исключить повторения кода в вьюсетах постов и комментариев.
    """

    # Проверяем изменение данных только автором.
    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужих данных запрещено!')
        super().perform_update(serializer)

    # Проверяем удаление данных только автором.
    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужих данных запрещено!')
        super().perform_destroy(instance)


class PostViewSet(AuthorizedModelViewSet):
    """Вьюсет для обработки постов."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # Переопределяем метод для автоматического добавления автора поста.
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    """Вьюсет для обработки групп."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(AuthorizedModelViewSet):
    serializer_class = CommentSerializer

    # Переопределяем получение объекта поста с комментариями.
    def get_queryset(self):
        """Проверяем наличие поста и возвращаем объект с комментариями."""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments

    # Переопределяем метод для автоматического добавления автора поста.
    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)
