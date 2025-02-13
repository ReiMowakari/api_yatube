from rest_framework.serializers import (
    ModelSerializer, SlugRelatedField)

from posts.models import Post, Group, Comment


class PostSerializer(ModelSerializer):
    """Сериалайзер для модели Post."""
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = (
            'id', 'text', 'author', 'image', 'group', 'pub_date'
        )


class GroupSerializer(ModelSerializer):
    """Сериалайзер для модели Group."""

    class Meta:
        model = Group
        fields = (
            'id', 'title', 'slug', 'description'
        )


class CommentSerializer(ModelSerializer):
    """Сериалайзер для модели Group."""
    author = SlugRelatedField(slug_field='username', read_only=True)
    post = SlugRelatedField(slug_field='id', read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id', 'author', 'post', 'text', 'created'
        )
