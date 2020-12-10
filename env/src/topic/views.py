from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateTopicPostForm, UpdateTopicPostForm
from account.models import Account
from .models import TopicPost
from django.db.models import F, Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from achievements.views import add_achievement
from forum_analytics.views import saveAnalytics


# Create your views here.
def checkDSAchievement(request):
    topicsByUser = TopicPost.objects.filter(author=request.user).count()
    if topicsByUser == 1:
        add_achievement(request=request, achievement='DS', level=1)
    elif topicsByUser == 10:
        add_achievement(request=request, achievement='DS', level=2)
    elif topicsByUser == 50:
        add_achievement(request=request, achievement='DS', level=3)
    elif topicsByUser == 100:
        add_achievement(request=request, achievement='DS', level=4)
    else:
        return True

def checkLikesAchievement(topic):
    if topic.total_likes() == 10:
        add_achievement(userWithAchievement=topic.author, achievement='TU', level=1)
    elif topic.total_likes() == 50:
        add_achievement(userWithAchievement=topic.author, achievement='TU', level=2)
    elif topic.total_likes() == 100:
        add_achievement(userWithAchievement=topic.author, achievement='TU', level=3)
    elif topic.total_likes() == 500:
        add_achievement(userWithAchievement=topic.author, achievement='CEL', level=1)
    elif topic.total_likes() == 1000:
        add_achievement(userWithAchievement=topic.author, achievement='CEL', level=2)
    elif topic.total_likes() == 2000:
        add_achievement(userWithAchievement=topic.author, achievement='CEL', level=3)
    else:
        return True

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
        checkDSAchievement(request)
        context['success'] = True
        form = CreateTopicPostForm()
        return redirect('home')
    else:
        context['failed'] = True
        form.initial={"title": request.POST.get("title"), "tags": request.POST.get("tags"), "body":  request.POST.get("body"), "category" : request.POST.get("category"), "is_approved" :request.POST.get("is_approved") }
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
        msg = "topic delete_post_view threw exception " + str(err) 
        saveAnalytics(request =None, log_key="Exception Thrown", log_value=msg, log_type='E', resolved=False)
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
            form.initial={"title": topic_post.title, "tags": topic_post.tags, "body":  topic_post.body, "featured_image" : topic_post.featured_image, "extra_image_one" : topic_post.extra_image_one, "extra_image_two" : topic_post.extra_image_two, "extra_image_three" : topic_post.extra_image_three, "category" : topic_post.category, "category_display" : topic_post.get_category_display(), "is_approved" : topic_post.is_approved  }
        else:
            context['failed'] = True
            form.initial={"title": request.POST.get("title"), "tags": request.POST.get("tags"), "body":  request.POST.get("body") , "featured_image" : topic_post.featured_image, "extra_image_one" : topic_post.extra_image_one, "extra_image_two" : topic_post.extra_image_two, "extra_image_three" : topic_post.extra_image_three, "category" : topic_post.category, "category_display" : topic_post.get_category_display(), "is_approved" : topic_post.is_approved }

    form = UpdateTopicPostForm(
                            initial={
                            "title": topic_post.title,
                            "tags": topic_post.tags,
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
        msg = "topic increment_view_count threw exception " + str(err) 
        saveAnalytics(request =None, log_key="Exception Thrown", log_value=msg, log_type='E', resolved=False)

POSTS_PER_PAGE = 20
def search_topics(query=None, page=1):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = TopicPost.objects.filter(Q(title__contains=q)|Q(tags__contains=q)|Q(body__icontains=q)).order_by('-date_updated').distinct()
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

def get_all_topics_by_author(request, page, author_id):
    author = get_object_or_404(Account, id=author_id)
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

def get_all_topics_by_tag(request, page, tag):
    queryset = []
    posts = TopicPost.objects.filter(Q(tags__contains=tag)).order_by('-date_updated').distinct()
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

def get_top_viewed_topics():
    return TopicPost.objects.all().order_by('-views')[:5]

def get_most_liked_topics():
    return TopicPost.objects.filter(likes__gt=0).order_by('-likes')[:5]

def get_topic_post_or_404(slug):
    return get_object_or_404(TopicPost, slug=slug)

def user_likes_topic_post(user, topic):
    return user in topic.likes.all()

def get_posts_liked_by_user(request, user):
    return TopicPost.objects.filter(likes__in=[user.id])[:10]

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
        checkLikesAchievement(topic)
    except Exception as err:
        msg = "topic like_topic_post threw exception " + str(err) 
        saveAnalytics(request =None, log_key="Exception Thrown", log_value=msg, log_type='E', resolved=False)

def dislike_topic_post(user, slug):
    if not user.is_authenticated:
        return redirect('must_authenticate')
    topic = get_object_or_404(TopicPost, slug=slug)
    try:
        topic.dislikes.add(user)
        topic.likes.remove(user)
    except Exception as err:
        msg = "topic dislike_topic_post threw exception " + str(err) 
        saveAnalytics(request =None, log_key="Exception Thrown", log_value=msg, log_type='E', resolved=False)