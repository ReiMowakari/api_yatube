from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from posts.models import Post, Group


class AuthorizedModelMixin(ModelViewSet):
    """
    Базовый миксин для авторизованного автора для изменения собственных данных.
    Вынес в отдельный миксин, основанный на ModelViewSet для того,
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


class PostViewSet(AuthorizedModelMixin):
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


class CommentViewSet(AuthorizedModelMixin):
    serializer_class = CommentSerializer

    # Добавляем метод для получения отдельного поста.
    def get_post(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post

    # Переопределяем получение объекта поста с комментариями.
    def get_queryset(self):
        """Проверяем наличие поста и возвращаем объект с комментариями."""
        return self.get_post().comments.all()

    # Переопределяем метод для автоматического добавления автора поста.
    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=self.get_post())
