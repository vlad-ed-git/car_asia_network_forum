from django.urls import path
from .views import(
    create_blog_view,
    my_blog_posts_view,
    edit_post_view,
    delete_post_view,
)

app_name = 'blog'
urlpatterns = [
    path('create/', create_blog_view, name='create'),
    path('my_posts/', my_blog_posts_view, name='my_posts'),
    path('edit_post/<str:slug>/', edit_post_view , name='edit_post'),
    path('delete_post/<str:slug>/<str:redirect_to>/', delete_post_view , name='delete_post'),
]
