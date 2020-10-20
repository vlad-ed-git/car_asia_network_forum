from django.urls import path
from .views import(
    ajax_comment_post,
    ajax_get_topic_comments,
    my_comments_posts_view,
    edit_post_view,
    delete_post_view,
)

app_name = 'comments'
urlpatterns = [
    path('create/', ajax_comment_post, name='create'),
    path('get_topic_comments/<int:post_id>/<int:page>/', ajax_get_topic_comments, name='get_topic_comments'),
    path('my_comments/', my_comments_posts_view, name='my_comments'),
    path('edit_comments/<str:slug>/', edit_post_view , name='edit_comments'),
    path('delete_comments/<str:slug>/<str:redirect_to>/', delete_post_view , name='delete_comments'),
]
