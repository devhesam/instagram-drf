from django.urls import path

from rest_framework import routers

from .views import UserRegister,FollowCrud

router=routers.DefaultRouter()
router.register('follow-action',FollowCrud,basename='follow-action')
# router.register('unfollow',UnFollowViewset,basename='unfollow')

urlpatterns = [
    path('register',UserRegister.as_view(),name='register'),
    # path('unfollow',UnFollowViewset.as_view(),name='unfollow'),
    # path('flower',CustomFlower.as_view(),name='flower')
]
urlpatterns+=router.urls