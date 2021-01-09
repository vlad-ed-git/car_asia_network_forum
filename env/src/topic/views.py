from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateTopicPostForm, UpdateTopicPostForm
from account.models import Account
from .models import TopicPost, CustomComment
from django.db.models import F, Q
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from topic.topic_categories import get_category_display, get_all_categories_and_displays
from dashboard.search_views import get_side_bar_announcements


# Create your views here.
def get_context_with_side_bar(request):
    context = {}
    context['categories'] = get_all_categories_and_displays()
    
    limit  = 10
    context['top_viewed_posts'] =TopicPost.objects.filter(is_approved=True, views__gte=1).order_by('-views')[:limit]
   
    if request.user.is_authenticated:
        user = request.user
        context['my_liked_posts'] = TopicPost.objects.filter(is_approved=True, likes__in=[user.id]).order_by('-date_updated')[:limit]
    context['top_liked_posts'] =  TopicPost.objects.filter(is_approved=True, likes__gte=1).order_by('-likes')[:limit]
    
    context['total_comments_stats'] = CustomComment.objects.filter(is_removed=False).count()
    context['total_posts_stats'] = TopicPost.objects.filter(is_approved=True).count()
    context['total_users_stats'] = Account.objects.filter(is_staff=False).count()
    return context

def handler404(request, exception):
    return render(request, 'topic/error_pages/404.html', status=404)

def handler500(request):
    return render(request, 'topic/error_pages/500.html', status=500)


def increment_views(request, post):
    TopicPost.objects.filter(slug = post.slug).update(views = F('views') + 1)
   
def like_post(request, slug):
    if request.user.is_authenticated:
        user = request.user
        post = get_object_or_404(TopicPost, slug = slug)
        post.likes.add(user)
        post.dislikes.remove(user)
    return redirect('post_details', slug = slug)

def dislike_post(request, slug):
    if request.user.is_authenticated:
        user = request.user
        post = get_object_or_404(TopicPost, slug = slug)
        post.dislikes.add(user)
        post.likes.remove(user)
    return redirect('post_details', slug = slug)
        
def checkIfUserDislikesPost(user, post):
    return user in post.dislikes.all()

def checkIfUserLikesPost(user, post):
    return user in post.likes.all()
    
def post_details_view(request, slug):
    context = get_context_with_side_bar(request)
    post = get_object_or_404(TopicPost, slug=slug)
    context['post'] = post
    if request.user.is_authenticated:
        user = request.user
        context['user_dislikes_post'] = checkIfUserDislikesPost(user, post)
        context['user_likes_post'] = checkIfUserLikesPost(user, post)
        if user.is_editor or (post.author == user):
            context['can_edit'] = True
    increment_views(request, post)
    return render(request, 'topic/website/post_page.html', context)



  
def home_view(request, query = None, category = None, author_id=None, tag = None, liked=None, page=1):
    context = get_context_with_side_bar(request)
    context['announcements'] = get_side_bar_announcements(request)
    if request.GET:
        query = str(request.GET.get("query"))
    
    if category:
        context['filter_by_category'] = get_category_display(category)
        context['filter_by_category_value'] = category
        context['posts'] = filter_all_posts_by_category(request=request, post_category=category, page=page)
    
    elif author_id:
        author = get_object_or_404(Account, id=author_id)
        context['filter_by_author'] = author.display_name
        context['filter_by_author_id'] = author_id
        context['posts'] = get_all_posts_by_author_id(request=request, author_id=author_id, page=page)
    elif tag:
        context['filter_by_tag'] = '#'+ tag
        context['filter_tag'] = tag
        context['posts'] = get_posts_tagged(request=request, tag=tag, page=page)
    
    elif liked == 1:
        context['filter_favorites'] = True
        context['posts'] = get_my_favorite_posts(request=request, page=page)
    
    elif query:
        context['filter_by_query'] = query
        context['posts'] = get_all_posts_with_query(request=request, query=query, page=page) 

    else:
        #get all
        context['posts'] = get_all_posts(request, page) 
    if context['posts']:
        context['total_results'] = len(context['posts'])
    else:
        context['total_results'] = 0
    
    return render(request, 'topic/website/home.html', context)

############## CRUD #################
def delete_topic_view(request, slug, confirmed=0):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    topic_post = get_object_or_404(TopicPost, slug=slug)
    if topic_post.author != user and not user.is_editor:
        return HttpResponse("You are not the author of that post")
    if confirmed == 0:
       #need to confirm
       context['post'] = topic_post
       return render(request, 'topic/user_pages/delete.html', context)
    elif confirmed == 1: 
       context['deleted'] = True  
       topic_post.delete()
       return render(request, 'topic/user_pages/delete.html', context)
    else:
        return redirect('home')
        
    
def create_topic_view(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
    form = CreateTopicPostForm(request.POST or None, request.FILES or None )
    if request.POST:
        if form.is_valid():
            # we need to set the author property before we can save
            obj = form.save(commit=False)
            author = Account.objects.get(email=user.email)
            obj.author = author
            obj.save()
            context['success'] = True
            form = CreateTopicPostForm()
            return redirect('post_details', slug = obj.slug)
        else:
            context['failed'] = True
            form.initial={"title": request.POST.get("title"), "tags": request.POST.get("tags"), "body":  request.POST.get("body"), "category" : request.POST.get("category"), "is_approved" :request.POST.get("is_approved") }
    context['create_form'] = form
    return render(request, 'topic/user_pages/forms/create_topic.html', context)

def edit_topic_view(request, slug):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    topic_post = get_object_or_404(TopicPost, slug=slug)
    if topic_post.author != user and not user.is_editor:
        return HttpResponse("You are not the author of that post")
    if request.POST:
        form = UpdateTopicPostForm(request.POST or None, request.FILES or None, instance=topic_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success'] = True
            topic_post = obj
            return redirect('post_details', slug = topic_post.slug)
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
    context['post'] = topic_post
    return render(request, 'topic/user_pages/forms/update_topic.html', context)












############## SEARCH AND FILTER AND PAGINATION ###########
RESULTS_PER_PAGE = 20
def get_paginated_results(results, page, sort_by=None):
    if not results:
        return None
    if sort_by:
        found_posts = sorted(list(set(results)),
                             key=attrgetter(sort_by), reverse=True)
    else:
        found_posts = results

    # Pagination
    found_posts_paginator = Paginator(found_posts, RESULTS_PER_PAGE)
    try:
        found_posts = found_posts_paginator.page(page)
    except PageNotAnInteger:
        found_posts = found_posts_paginator.page(RESULTS_PER_PAGE)
    except EmptyPage:
        found_posts = found_posts_paginator.page(
            found_posts_paginator.num_pages)
    return found_posts


def get_all_posts(request, page):
    try:
        if request.user.is_authenticated and request.user.is_editor:
            posts = TopicPost.objects.all().order_by('-date_updated')
            
        else:
            # get only approved posts
            posts = TopicPost.objects.filter(is_approved=True).order_by('-date_updated')
        return get_paginated_results(posts, page)
    except Exception as err:
        print(str(err))
        return None
    
def filter_all_posts_by_category(request, post_category, page=1):
    if not post_category:
        return None
    try:
        if request.user.is_authenticated and request.user.is_editor:
            posts = TopicPost.objects.filter(category=post_category).order_by('-date_updated')
        else:
            # get only approved posts
            posts = TopicPost.objects.filter(is_approved=True,category=post_category).order_by('-date_updated')

        return get_paginated_results(posts, page)
    except Exception as err:
        print(str(err))
        return None

def get_all_posts_by_author_id(request, author_id, page=1):
    if not author_id:
        return None
    try:
        author = Account.objects.get(pk=author_id)
        posts_set = False
        if request.user.is_authenticated:
            user = request.user
            if user.is_editor or (user.id == author_id):
                posts_set = True
                posts = TopicPost.objects.filter(author=author).order_by('-date_updated')
        
        if not posts_set:
            # get only approved posts
            posts = TopicPost.objects.filter(is_approved=True,author=author).order_by('-date_updated')

        return get_paginated_results(posts, page)
    except Exception as err:
        print(str(err))
        return None
  
def get_my_favorite_posts(request, page=1):
    if not request.user.is_authenticated:
        return None
    try:
        user = request.user
        posts = TopicPost.objects.filter(is_approved=True,likes__in=[user.id]).order_by('-date_updated')

        return get_paginated_results(posts, page)
    except Exception as err:
        print(str(err))
        return None
    
def get_posts_tagged(request, tag, page=1):
    try:
        if request.user.is_authenticated and request.user.is_editor:
            posts = TopicPost.objects.filter(Q(tags__icontains=tag)).order_by('-date_updated')
        else:
            posts = TopicPost.objects.filter(Q(is_approved=True),Q(tags__icontains=tag)).order_by('-date_updated')

        return get_paginated_results(posts, page)
    except Exception as err:
        print(str(err))
        return None
    

def get_all_posts_with_query(request, query, page=1):
    if not query:
        return None
    queryset = []
    queries = query.split(" ")
    for q in queries:
        if request.user.is_authenticated and request.user.is_editor:
            posts = TopicPost.objects.filter(Q(title__icontains=q) | Q(
                body__icontains=q) |  Q(tags__icontains=q)).distinct()

        else:
            # get only approved posts
            posts = TopicPost.objects.filter(Q(is_approved=True), Q(title__icontains=q) | Q(body__icontains=q) | Q(tags__icontains=q)
                                                  ).distinct()

        for post in posts:
            queryset.append(post)
    return get_paginated_results(queryset, page, sort_by='date_updated')