
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import viewsets, permissions

from user.models import Follow
from .serializer import UserRegisterSerailizer,\
     FollowingSerializer, FollowerSerializer


class UserRegister(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserRegisterSerailizer

    def create(self, request, *args, **kwargs):
        if request.data['passwordConfirmation'] != request.data['password']:
            return Response({'password': 'Password does not match'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['passwordConfirmation'] = self.request.data['passwordConfirmation']
        return context


class FollowCrud(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['POST'], detail=True, url_path='follow')
    def follow_request_received(self, request, pk):
        print(request.user)
        user_send_request: Follow = get_object_or_404(get_user_model(), id=pk)
        """ following operation"""
        if not Follow.objects.filter(user=request.user, following=user_send_request).exists():
            Follow.objects.create(
                user=request.user, following=user_send_request)
        """follower operation"""
        if not Follow.objects.filter(user=user_send_request, followers=request.user).exists():
            Follow.objects.create(user=user_send_request,followers=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_226_IM_USED)

    @action(methods=['POST'], detail=True, url_path='accept-follow-request')
    def accept_follow_request(self, request, pk):
        user: Follow = Follow.objects.filter(Q(user=request.user) & Q(
            following_id=pk) | Q(followers_id=pk)).update(status='accept')
        if user:
            user = get_user_model().objects.get(id=pk)
            Follow.objects.filter(
                user=user, following=request.user).update(status='accept')
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['POST'], detail=True, url_path='unfollow')
    def unfollow(self, request, pk):
        user: Follow = Follow.objects.filter(
            Q(user=request.user) & Q(following_id=pk) | Q(followers_id=pk))
        if user:
            user.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=False, url_path='list-following')
    def following_list(self, request):
        following = Follow.objects.filter(
            user=request.user, status='accept').exclude(following__isnull=True)
        serializer = FollowingSerializer(following, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='list-follower')
    def follower_list(self, request):
        print(request.user)
        following = Follow.objects.filter\
            (user=request.user, status='accept',).exclude(followers__isnull=True)
        serializer = FollowerSerializer(following, many=True)
        return Response(serializer.data)
