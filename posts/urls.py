from django.urls import path

from posts.views import PostView,PostsDetailView,AddCommentView,ManageCommentView,ShowPostLikesComments,LikeCreateView,GetLikersView

urlpatterns = [
    path('posts/', PostView.as_view(), name='posts'),
    path('posts/<int:pk>/', PostsDetailView.as_view(), name='post'),
    path('add-comment/<int:post_id>/<int:user_id>', AddCommentView.as_view(), name='add-comment'),
    path('manage-comment/<int:comment_id>', ManageCommentView.as_view(), name='manage-comment'),
    path('show-likes-comments/', ShowPostLikesComments.as_view(), name='show-likes-comments'),
    path('add-like/<int:post_id>', LikeCreateView.as_view(), name='add-like'),
    path('get-likers/<int:post_id>', GetLikersView.as_view(), name='get-likers'),
]
