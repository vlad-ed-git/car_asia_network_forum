"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from account.views import(
    profile_view,
    must_authenticate_view,
)

from topic.views import(
    create_topic_view,
    edit_topic_view,
    home_view,
    post_details_view,
    dislike_post,
    like_post,
    delete_topic_view,
    handler404,
    handler500,
)

from dashboard.views import(
    announcement_details_view,
    create_announcement_view,
    edit_announcement_view,
    delete_announcement_view,
    announcements_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #account
    path('api/account/', include('account.api.urls'), name= 'account_api'),
    path('profile/', profile_view, name="profile"),
    path('must_authenticate/' , must_authenticate_view, name="must_authenticate"),
    
    #topic
    path('', home_view, name="home"),
    path('create/', create_topic_view, name='create'),
    path('edit/<str:slug>/', edit_topic_view, name='edit'),
    path('delete/<int:confirmed>/<str:slug>/', delete_topic_view, name='delete'),
    path('all/<int:page>/', home_view, name='all_posts'),
    path('search/<str:query>/<int:page>/', home_view, name='search'),
    path('filter/<str:category>/<int:page>/', home_view, name='filter'),
    path('author_posts/<int:author_id>/<int:page>/', home_view, name='author_posts'),
    path('tags/<str:tag>/<int:page>/', home_view, name='tagged'),
    path('favorites/<int:liked>/<int:page>/', home_view, name='favorites'),
    path('post/<str:slug>/', post_details_view, name='post_details'), 
    path('like/<str:slug>/', like_post, name='like'),
    path('dislike/<str:slug>/', dislike_post, name='dislike'),
     
    #annoucements
    path('announcements/<int:page>/', announcements_view, name='announcements' ),
    path('announcements/<int:author_id>/<int:page>/', announcements_view, name='authors_announcements'),
    path('announcement/<str:slug>/', announcement_details_view, name='announcement_details'),
    path('create_announcement/', create_announcement_view, name='create_announcement'),
    path('edit_announcement/<str:slug>/', edit_announcement_view, name='edit_announcement'),
    path('delete_announcement/<int:confirmed>/<str:slug>/', delete_announcement_view, name='delete_announcement'),
    
    #comments
    path('comments/', include('django_comments_xtd.urls'), name="topic_comments"),  
    
    
    #language 
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
handler404 = handler404
handler500 = handler500