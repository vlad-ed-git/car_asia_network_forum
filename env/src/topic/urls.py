from django.urls import path
from .views import(
    create_topic_view,
    my_topic_posts_view,
    edit_post_view,
    delete_post_view,
)

app_name = 'topic'
urlpatterns = [
    path('create/', create_topic_view, name='create'),
    path('my_topics/', my_topic_posts_view, name='my_topics'),
    path('edit_topic/<str:slug>/', edit_post_view , name='edit_topic'),
    path('delete_topic/<str:slug>/<str:redirect_to>/', delete_post_view , name='delete_topic'),
]
