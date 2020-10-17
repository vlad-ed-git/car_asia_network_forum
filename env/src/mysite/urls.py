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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


from account.views import(
    registration_view,
    login_view,
    logout_view,
    profile_view,
    must_authenticate_view
)

from website.views import (
    home_view,
    post_details_view,
    like_post_view,
    dislike_post_view,
    handler404,
    handler500,

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    path('authors_posts/<str:posts_by_author>/<str:post_type>/',home_view, name='authors_posts'),
    path('post_details/<str:post_type>/<str:slug>/', post_details_view, name='post_details'),
    path('like_post/<str:slug>/<str:post_type>/', like_post_view , name='like_post'),
    path('dislike_post/<str:slug>/<str:post_type>/', dislike_post_view , name='dislike_post'),
    
    #blog views
    path('blog/', include('blog.urls'), name='blog'),
    path('discussions/', include('topic.urls'), name='topic'),

    #user auth views
    path('register/', registration_view, name="register"),
    path('login/', login_view, name="login"),
    path('profile/', profile_view, name="profile"),
    path('logout/', logout_view, name="logout"),
    path('must_authenticate/' , must_authenticate_view, name="must_authenticate"),

    #REST FRAMEWORK URLS
    path('api/blog/', include('blog.api.urls'), name= 'blog_api'),
    path('api/account/', include('account.api.urls'), name= 'account_api'),

    # Password reset links
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_reset/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='account/password_reset/password_change.html'),
         name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset/password_reset_complete.html'),
         name='password_reset_complete'),
]

handler404 = handler404
handler500 = handler500

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
