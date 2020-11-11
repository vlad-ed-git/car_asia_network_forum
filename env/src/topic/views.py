from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateTopicPostForm, UpdateTopicPostForm
from account.models import Account
from .models import TopicPost
from django.db.models import F, Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse


# Create your views here.
def get_topic_categories(request):
    choices  = TopicPost._meta.get_field('category').choices
    return choices

def create_topic_view(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
    form = CreateTopicPostForm(request.POST or None, request.FILES or None )
    if form.is_valid():
        # we need to set the author property before we can save
        obj = form.save(commit=False)
        author = Account.objects.get(email=user.email)
        obj.author = author
        obj.save()
        context['success'] = True
        form = CreateTopicPostForm()
        return redirect('home')
    else:
        context['failed'] = True
        form.initial={"title": request.POST.get("title"), "body":  request.POST.get("body"), "category" : request.POST.get("category"), "is_approved" :request.POST.get("is_approved") }
    context['create_form'] = form
    return render(request, 'website/app_pages/topic/create_topic.html', context)


def my_topic_posts_view(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
    context['is_my_posts'] = True
    querySet = TopicPost.objects.filter(author=user).order_by('-date_updated')
    posts = []
    for post in querySet:
        posts.append(post)
    context["posts"] =  posts
    return render(request, 'website/app_pages/topic/my_topics.html', context)

def delete_post_view(request, slug, redirect_to):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
    try:
        post = TopicPost.objects.get(slug=slug)
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

    topic_post = get_object_or_404(TopicPost, slug=slug)
    if topic_post.author != user and not user.is_super_editor:
        return HttpResponse("You are not the author of that post")
    if request.POST:
        form = UpdateTopicPostForm(request.POST or None, request.FILES or None, instance=topic_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success'] = True
            topic_post = obj
            form.initial={"title": topic_post.title, "body":  topic_post.body, "featured_image" : topic_post.featured_image, "extra_image_one" : topic_post.extra_image_one, "extra_image_two" : topic_post.extra_image_two, "extra_image_three" : topic_post.extra_image_three, "category" : topic_post.category, "category_display" : topic_post.get_category_display(), "is_approved" : topic_post.is_approved  }
        else:
            context['failed'] = True
            form.initial={"title": request.POST.get("title"), "body":  request.POST.get("body") , "featured_image" : topic_post.featured_image, "extra_image_one" : topic_post.extra_image_one, "extra_image_two" : topic_post.extra_image_two, "extra_image_three" : topic_post.extra_image_three, "category" : topic_post.category, "category_display" : topic_post.get_category_display(), "is_approved" : topic_post.is_approved }

    form = UpdateTopicPostForm(
                            initial={
                            "title": topic_post.title,
                            "body": topic_post.body,
                            "featured_image" : topic_post.featured_image,
                            "extra_image_one" : topic_post.extra_image_one,
                            "extra_image_two" : topic_post.extra_image_two,
                            "extra_image_three" : topic_post.extra_image_three,
                            "category" : topic_post.category,
                            "category_display" : topic_post.get_category_display(), "is_approved" : topic_post.is_approved
                            })
    context['update_form'] = form
    return render(request, 'website/app_pages/topic/update_topic.html', context)


def increment_view_count(slug):
    try:
        TopicPost.objects.filter(slug = slug).update(views = F('views') + 1)
    except Exception as err:
        print("incrementing topic post view count" + str(err))

POSTS_PER_PAGE = 10
def search_topics(query=None, page=1):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = TopicPost.objects.filter(Q(title__contains=q)|Q(body__icontains=q)).order_by('-date_updated').distinct()
        for post in posts:
            queryset.append(post)
    # create unique set and then convert to list
    topic_posts_paginator = Paginator(queryset, POSTS_PER_PAGE)
    try:
        topicPosts = topic_posts_paginator.page(page)
    except PageNotAnInteger:
        topicPosts = topic_posts_paginator.page(POSTS_PER_PAGE)
    except EmptyPage:
        topicPosts = topic_posts_paginator.page(topic_posts_paginator.num_pages)
    return topicPosts


def get_all_topics(request, page):
    topic_posts =  TopicPost.objects.all().order_by('-date_updated')
    topic_posts_paginator = Paginator(topic_posts, POSTS_PER_PAGE)
    try:
        topicPosts = topic_posts_paginator.page(page)
    except PageNotAnInteger:
        topicPosts = topic_posts_paginator.page(POSTS_PER_PAGE)
    except EmptyPage:
        topicPosts = topic_posts_paginator.page(topic_posts_paginator.num_pages)
    return topicPosts

def get_all_topics_by_author(request, page, username):
    author = get_object_or_404(Account, username=username)
    topic_posts =  TopicPost.objects.filter(author=author).order_by('-date_updated')
    topic_posts_paginator = Paginator(topic_posts, POSTS_PER_PAGE)
    try:
        topicPosts = topic_posts_paginator.page(page)
    except PageNotAnInteger:
        topicPosts = topic_posts_paginator.page(POSTS_PER_PAGE)
    except EmptyPage:
        topicPosts = topic_posts_paginator.page(topic_posts_paginator.num_pages)
    return topicPosts

def get_all_topics_by_category(request, page, category):
    topic_posts =  TopicPost.objects.filter(category=category).order_by('-date_updated')
    topic_posts_paginator = Paginator(topic_posts, POSTS_PER_PAGE)
    try:
        topicPosts = topic_posts_paginator.page(page)
    except PageNotAnInteger:
        topicPosts = topic_posts_paginator.page(POSTS_PER_PAGE)
    except EmptyPage:
        topicPosts = topic_posts_paginator.page(topic_posts_paginator.num_pages)
    return topicPosts

def get_top_viewed_topics():
    return TopicPost.objects.all().order_by('-views')[:5]

def get_most_liked_topics():
    return TopicPost.objects.filter(likes__gt=0).order_by('-likes')[:5]

def get_topic_post_or_404(slug):
    return get_object_or_404(TopicPost, slug=slug)

def user_likes_topic_post(user, topic):
    return user in topic.likes.all()

def user_dislikes_topic_post(user, topic):
    return user in topic.dislikes.all()

def user_owns_topic_post(user, topic):
    return topic.author == user

def like_topic_post(user, slug):
    if not user.is_authenticated:
        return redirect('must_authenticate')
    topic = get_object_or_404(TopicPost, slug=slug)
    try:
        topic.likes.add(user)
        topic.dislikes.remove(user)
    except Exception as err:
        print(str(err))

def dislike_topic_post(user, slug):
    if not user.is_authenticated:
        return redirect('must_authenticate')
    topic = get_object_or_404(TopicPost, slug=slug)
    try:
        topic.dislikes.add(user)
        topic.likes.remove(user)
    except Exception as err:
        print(str(err))