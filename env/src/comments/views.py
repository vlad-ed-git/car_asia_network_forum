from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateCommentsPostForm, UpdateCommentsPostForm
from account.models import Account
from topic.models import TopicPost
from .models import CommentsPost
from django.db.models import F, Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from django.core import serializers

# Create your views here.
def ajax_comment_post(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
    if request.is_ajax and request.method == "POST":
        form = CreateCommentsPostForm(request.POST or None, request.FILES or None )
        if form.is_valid():
            try:
                # we need to set the author property before we can save
                obj = form.save(commit=False)
                author = Account.objects.get(email=user.email)
                obj.author = author
                obj.save()
                # send to client side.
                return JsonResponse({"success": "Your comment has been posted"}, status=200)
            except Exception as err:
                print("-------------------------------err------------")
                print(str(err))
                errorMsg = "You may have already made that comment!"
        else:
           errorMsg = "Invalid comment!"
    else:
        errorMsg = "Only ajax post method is supported"
    return JsonResponse({"error": errorMsg}, status=400)


def my_comments_posts_view(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
    context['is_my_posts'] = True
    querySet = CommentsPost.objects.filter(author=user).order_by('-date_updated')
    posts = []
    for post in querySet:
        posts.append(post)
    context["posts"] =  posts
    return render(request, 'website/app_pages/comments/my_comments.html', context)

def delete_post_view(request, slug, redirect_to):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
    try:
        post = CommentsPost.objects.get(slug=slug)
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

    comments_post = get_object_or_404(CommentsPost, slug=slug)
    if comments_post.author != user and not user.is_super_editor:
        return HttpResponse("You are not the author of that post")
    if request.POST:
        form = UpdateCommentsPostForm(request.POST or None, request.FILES or None, instance=comments_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success'] = True
            comments_post = obj
            form.initial={"body":  comments_post.body, "for_post_id" : comments_post.for_post_id,"is_response_to_topic" : comments_post.is_response_to_topic,"is_response_to_comment" : comments_post.is_response_to_comment, "is_approved" : comments_post.is_approved  }
        else:
            context['failed'] = True
            form.initial={ "body":  request.POST.get("body") , "for_post_id" : request.POST.get("for_post_id"),"is_response_to_topic" : request.POST.get("is_response_to_topic"),"is_response_to_comment" : request.POST.get("is_response_to_comment"), "is_approved" : comments_post.is_approved }

    form = UpdateCommentsPostForm(
                            initial={
                            "body": comments_post.body,
                            "for_post_id" : comments_post.for_post_id,
                            "is_response_to_topic" : comments_post.is_response_to_topic,
                            "is_response_to_comment" : comments_post.is_response_to_comment, 
                            "is_approved" : comments_post.is_approved
                            })
    context['update_form'] = form
    return render(request, 'website/app_pages/comments/update_comments.html', context)


def increment_view_count(slug):
    try:
        CommentsPost.objects.filter(slug = slug).update(views = F('views') + 1)
    except Exception as err:
        print("incrementing comments post view count" + str(err))

POSTS_PER_PAGE = 10
def search_comments(query=None, page=1):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = CommentsPost.objects.filter(Q(body__icontains=q)).order_by('-date_updated').distinct()
        for post in posts:
            queryset.append(post)
    # create unique set and then convert to list
    comments_posts_paginator = Paginator(queryset, POSTS_PER_PAGE)
    try:
        commentsPosts = comments_posts_paginator.page(page)
    except PageNotAnInteger:
        commentsPosts = comments_posts_paginator.page(POSTS_PER_PAGE)
    except EmptyPage:
        commentsPosts = comments_posts_paginator.page(comments_posts_paginator.num_pages)
    return commentsPosts


def get_all_comments(request, post_id, page):
    comments_posts =  CommentsPost.objects.filter(for_post_id=post_id).order_by('-date_updated')
    comments_posts_paginator = Paginator(comments_posts, POSTS_PER_PAGE)
    try:
        commentsPosts = comments_posts_paginator.page(page)
    except PageNotAnInteger:
        commentsPosts = comments_posts_paginator.page(POSTS_PER_PAGE)
    except EmptyPage:
        commentsPosts = comments_posts_paginator.page(comments_posts_paginator.num_pages)
    return commentsPosts

def get_all_comments_by_author(request, page, username):
    author = get_object_or_404(Account, username=username)
    comments_posts =  CommentsPost.objects.filter(author=author).order_by('-date_updated')
    comments_posts_paginator = Paginator(comments_posts, POSTS_PER_PAGE)
    try:
        commentsPosts = comments_posts_paginator.page(page)
    except PageNotAnInteger:
        commentsPosts = comments_posts_paginator.page(POSTS_PER_PAGE)
    except EmptyPage:
        commentsPosts = comments_posts_paginator.page(comments_posts_paginator.num_pages)
    return commentsPosts

def get_top_viewed_comments():
    return CommentsPost.objects.all().order_by('-views')[:5]

def get_most_liked_comments():
    return CommentsPost.objects.filter(likes__gt=0).order_by('-likes')[:5]

def get_comments_post_or_404(slug):
    return get_object_or_404(CommentsPost, slug=slug)

def user_likes_comments_post(user, comments):
    return user in comments.likes.all()

def user_dislikes_comments_post(user, comments):
    return user in comments.dislikes.all()

def user_owns_comments_post(user, comments):
    return comments.author == user

def like_comments_post(user, slug):
    if not user.is_authenticated:
        return redirect('must_authenticate')
    comments = get_object_or_404(CommentsPost, slug=slug)
    try:
        comments.likes.add(user)
        comments.dislikes.remove(user)
    except Exception as err:
        print(str(err))

def dislike_comments_post(user, slug):
    if not user.is_authenticated:
        return redirect('must_authenticate')
    comments = get_object_or_404(CommentsPost, slug=slug)
    try:
        comments.dislikes.add(user)
        comments.likes.remove(user)
    except Exception as err:
        print(str(err))