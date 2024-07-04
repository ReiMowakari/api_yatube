from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from posts.models import Post, Group


class AuthorizedModelMixin:
    """
    Базовый миксин для авторизованного автора для изменения собственных данных.
    Вынес в отдельный миксин, для того,
    чтобы исключить повторения кода в вьюсетах постов и комментариев.
    """

    def perform_update(self, serializer):
        """
        Проверяем изменение данных только автором.
        :param serializer:
        :return: обновление объекта.
        """
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужих данных запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """
        Проверяем удаление данных только автором.
        :param instance:
        :return: удаление объекта.
        """
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужих данных запрещено!')
        super().perform_destroy(instance)


class PostViewSet(AuthorizedModelMixin, ModelViewSet):
    """Вьюсет для обработки постов."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """
        Переопределяем метод для автоматического добавления автора поста.
        :param serializer:
        :return: создаем объект поста.
        """
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    """Вьюсет для обработки групп."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(AuthorizedModelMixin, ModelViewSet):
    serializer_class = CommentSerializer

    def get_post(self):
        """
        Метод для получения отдельного поста.
        :return:
        """
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post

    def get_queryset(self):
        """
        Проверяем наличие поста.
        :return: возвращаем объект с комментариями
        """
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """
        Переопределяем метод для автоматического добавления автора поста.
        :param serializer:
        :return: объект поста с автором.
        """
        serializer.save(
            author=self.request.user,
            post=self.get_post())
