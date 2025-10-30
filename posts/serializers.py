import datetime as dt
from rest_framework import serializers

from .models import Post, Group, Comment, User


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'posts')
        ref_name = 'ReadOnlyUsers'


class GroupSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='title')

    class Meta:
        model = Group
        fields = ('id', 'group_name', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    created = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created')

    def get_created(self, obj):
        return dt.datetime.strftime(obj.created, '%d.%m.%Y %H:%M:%S')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    comments = CommentSerializer(read_only=True, many=True)
    group = GroupSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group',
                  'comments')

    def create(self, validated_data):
        if 'group' not in self.initial_data:
            post = Post.objects.create(**validated_data)
        else:
            group_id = self.initial_data.pop('group')
            group = Group.objects.get(id=group_id)
            post = Post.objects.create(**validated_data)
            post.group = group
            post.save()
        return post

    def update(self, instance, validated_data):
        if 'group' in self.initial_data:
            group_id = self.initial_data.pop('group')
            if group_id is not None:
                group = Group.objects.get(id=group_id)
                instance.group = group
            instance.save()
        return super().update(instance, validated_data)
