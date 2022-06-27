from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Post,Comment


class PostlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = { 'user': {'read_only': True} }

    def create(self, validated_data):
        return Post.objects.create(user=self.context['user'],**validated_data)    
       


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = { 'user': {'read_only': True} }

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance       

class AuthorSerializer(serializers.ModelSerializer):
    """
    serializer to get user
    """
    class Meta:
        model = User
        fields = ('username',)


class CommentSerializer(serializers.ModelSerializer):
    """
    serializer to get comments
    """
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created_time')
        read_only_fields = ('author', 'id', 'created_time')


class NestedComment(serializers.ModelSerializer):
    """
    serializer to get comments for ShowLikesCommentsSerializer
    """
    author = serializers.CharField(source='author.username')

    class Meta:
        model = Comment
        exclude = ['id', 'post']


class ShowLikesCommentsSerializer(serializers.ModelSerializer):
    """
    serializer to get all likes and comments for all posts per user
    """
    posts_comments = NestedComment(read_only=True, many=True)
    creator = serializers.CharField(source='creator.username')
    likes = AuthorSerializer(read_only=True, many=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'creator', 'created_time', 'image', 'caption',
                  'posts_comments', 'likes', 'likes_count', 'comments_count']

    def get_comments_count(self, obj):
        return obj.posts_comments.count()