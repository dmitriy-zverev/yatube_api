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

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    post = serializers.IntegerField(source='post.id', read_only=True)
    created = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')

    def get_created(self, obj):
        return dt.datetime.strftime(obj.created, '%d.%m.%Y %H:%M:%S')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(),
                                               allow_null=True,
                                               required=False)

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        group_id = self.initial_data.get('group')
        group = None
        if group_id is not None:
            group = Group.objects.get(id=group_id)
        post.group = group
        post.save(update_fields=['group'])
        return post

    def update(self, instance, validated_data):
        if 'group' in self.initial_data:
            group_id = self.initial_data.pop('group')
            group = None
            if group_id is not None:
                group = Group.objects.get(id=group_id)
            instance.group = group
            instance.save()
        return super().update(instance, validated_data)
