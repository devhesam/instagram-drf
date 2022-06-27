from urllib import response
from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status, authentication
from rest_framework.generics import ListAPIView,get_object_or_404

from .serializer import PostlistSerializer, PostDetailSerializer,CommentSerializer,AuthorSerializer,ShowLikesCommentsSerializer
from .models import Post, Comment


class PostView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query_set = Post.objects.all()
        serializer = PostlistSerializer(query_set, many=True)
        return response(serializer.data)


    def post(self, request):
        serializer = PostlistSerializer(data=request.data,context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return response(serializer.data, status=201)
        return response(serializer.errors, status=400)    
    
######## way 1
# class PostDetailView(APIView):

#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, pk):
#         query_set = Post.objects.get(pk=pk)
#         serializer = PostlistSerializer(query_set)
#         return response(serializer.data)

#     def put(self, request, pk):
#         query_set = Post.objects.get(pk=pk)
#         serializer = PostDetailSerializer(query_set, data=request.data, context={'user': request.user}, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return response(serializer.data, status=201)
#         return response(serializer.errors, status=400)

#     def delete(self, request, pk):
#         query_set = Post.objects.get(pk=pk)
#         query_set.delete()
#         return response(status=204)    

#### way 2
class PostsDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class AddCommentView(APIView):

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id=None, user_id=None):
        follower_user = User.objects.get(id=request.user.id)
        user = get_object_or_404(User, id=user_id)
        query_follower = user.followers_table.followers.all()
        post = get_object_or_404(Post, pk=post_id)
        if query_follower.filter(follower=follower_user) or follower_user == user:
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(post=post, author=self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=403)


class ManageCommentView(RetrieveUpdateDestroyAPIView):
    """
    view to manage comments
    """
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'
    # authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        queryset = Comment.objects.all()
        return queryset


class ShowPostLikesComments(ListAPIView):
    """
    view to get all likes and comments and posts for each owner posts
    """
    serializer_class = ShowLikesCommentsSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.all().filter(creator=self.request.user).order_by('-created_time')
        return queryset


class LikeCreateView(APIView):
    """ toggle like """
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, post_id=None):
        post = get_object_or_404(Post, pk=post_id)
        user = self.request.user
        if user in post.likes.all():
            like = False
            post.likes.remove(user)
        else:
            like = True
            post.likes.add(user)
        data = {
            'like': like
        }
        return Response(data)


class GetLikersView(ListAPIView):
    """ view to get all likes for each post """
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AuthorSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        queryset = Post.objects.get(creator=self.request.user, pk=post_id).likes.all()
        return queryset
