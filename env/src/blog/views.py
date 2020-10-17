from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account
from .models import BlogPost
from django.db.models import F, Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse

# Create your views here.
def create_blog_view(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
    form = CreateBlogPostForm(request.POST or None, request.FILES or None )
    if form.is_valid():
        # we need to set the author property before we can save
        obj = form.save(commit=False)
        author = Account.objects.get(email=user.email)
        obj.author = author
        obj.save()
        context['success'] = True
        form = CreateBlogPostForm()
    else:
        context['failed'] = True
        form.initial={"title": request.POST.get("title"), "body":  request.POST.get("body") }
    context['create_form'] = form
    return render(request, 'website/app_pages/blog/create_blog.html', context)


def my_blog_posts_view(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
    context['is_my_posts'] = True
    querySet = BlogPost.objects.filter(author=user).order_by('-date_updated')
    posts = []
    for post in querySet:
        posts.append(post)
    context["posts"] =  posts
    return render(request, 'website/app_pages/blog/my_blogs.html', context)

def delete_post_view(request, slug, redirect_to):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
    try:
        post = BlogPost.objects.get(slug=slug)
        if post.author == user or user.is_super_editor:
            post.delete()
        else:
            return HttpResponse("You are not the author of that post")
    except Exception as err:
        print(str(err))
    return redirect(redirect_to)

def edit_post_view(request, slug):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    blog_post = get_object_or_404(BlogPost, slug=slug)
    if blog_post.author != user and not user.is_super_editor:
        return HttpResponse("You are not the author of that post")
    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success'] = True
            blog_post = obj
            form.initial={"title": blog_post.title, "body":  blog_post.body, "featured_image" : blog_post.featured_image, "extra_image_one" : blog_post.extra_image_one, "extra_image_two" : blog_post.extra_image_two, "extra_image_three" : blog_post.extra_image_three  }
        else:
            context['failed'] = True
            form.initial={"title": request.POST.get("title"), "body":  request.POST.get("body") , "featured_image" : blog_post.featured_image, "extra_image_one" : blog_post.extra_image_one, "extra_image_two" : blog_post.extra_image_two, "extra_image_three" : blog_post.extra_image_three}

    form = UpdateBlogPostForm(
                            initial={
                            "title": blog_post.title, 
                            "body": blog_post.body,
                            "featured_image" : blog_post.featured_image,
                            "extra_image_one" : blog_post.extra_image_one,
                            "extra_image_two" : blog_post.extra_image_two,
                            "extra_image_three" : blog_post.extra_image_three
                            })
    context['update_form'] = form
    return render(request, 'website/app_pages/blog/update_blog.html', context)


def increment_view_count(slug):
    try:
        BlogPost.objects.filter(slug = slug).update(views = F('views') + 1)
    except Exception as err:
        print("incrementing blog post view count" + str(err))

POSTS_PER_PAGE = 10
def search_blogs(query=None, page=1):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = BlogPost.objects.filter(Q(title__contains=q)|Q(body__icontains=q)).order_by('-date_updated').distinct()
        for post in posts:
            queryset.append(post)
    # create unique set and then convert to list
    blog_posts_paginator = Paginator(queryset, POSTS_PER_PAGE)
    try:
        blogPosts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blogPosts = blog_posts_paginator.page(POSTS_PER_PAGE)
    except EmptyPage:
        blogPosts = blog_posts_paginator.page(blog_posts_paginator.num_pages)
    return blogPosts


def get_all_blogs(request, page):
    blog_posts =  BlogPost.objects.all().order_by('-date_updated')
    blog_posts_paginator = Paginator(blog_posts, POSTS_PER_PAGE)
    try:
        blogPosts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blogPosts = blog_posts_paginator.page(POSTS_PER_PAGE)
    except EmptyPage:
        blogPosts = blog_posts_paginator.page(blog_posts_paginator.num_pages)
    return blogPosts

def get_all_blogs_by_author(request, page, username):
    author = get_object_or_404(Account, username=username)
    blog_posts =  BlogPost.objects.filter(author=author).order_by('-date_updated')
    blog_posts_paginator = Paginator(blog_posts, POSTS_PER_PAGE)
    try:
        blogPosts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blogPosts = blog_posts_paginator.page(POSTS_PER_PAGE)
    except EmptyPage:
        blogPosts = blog_posts_paginator.page(blog_posts_paginator.num_pages)
    return blogPosts

def get_top_viewed_blogs():
    return BlogPost.objects.all().order_by('-views')[:5]

def get_most_liked_blogs():
    return BlogPost.objects.filter(likes__gt=0).order_by('-likes')[:5]

def get_blog_post_or_404(slug):
    return get_object_or_404(BlogPost, slug=slug)

def user_likes_blog_post(user, blog):
    return user in blog.likes.all()

def user_dislikes_blog_post(user, blog):
    return user in blog.dislikes.all()

def user_owns_blog_post(user, blog):
    return blog.author == user

def like_blog_post(user, slug):
    if not user.is_authenticated:
        return redirect('must_authenticate')
    blog = get_object_or_404(BlogPost, slug=slug)
    try:
        blog.likes.add(user)
        blog.dislikes.remove(user)
    except Exception as err:
        print(str(err))

def dislike_blog_post(user, slug):
    if not user.is_authenticated:
        return redirect('must_authenticate')
    blog = get_object_or_404(BlogPost, slug=slug)
    try:
        blog.dislikes.add(user)
        blog.likes.remove(user)
    except Exception as err:
        print(str(err))