from django.shortcuts import get_object_or_404
from .models import AnnouncementPost
from django.db.models import F, Q
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

############## SEARCH AND FILTER AND PAGINATION ###########
#not paginated
def get_side_bar_announcements(request):
    limit = 10
    try:
        if request.user.is_authenticated:
            if request.user.is_super_editor:
                posts = AnnouncementPost.objects.all().order_by('-date_updated')[:limit]
            else:
                #only posts I have not yet seen
                posts = AnnouncementPost.objects.filter(is_approved=True).exclude(viewed_by__in=[user.id]).order_by('-date_updated')[:limit]
        else:
            # get only approved posts
            posts = AnnouncementPost.objects.filter(is_approved=True).order_by('-date_updated')[:limit]
        return posts
    except Exception as err:
        print(str(err))
        return None


### PAGINATED
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




def get_all_announcements(request, page=1):
    try:
        if request.user.is_authenticated:
            if request.user.is_super_editor:
                posts = AnnouncementPost.objects.all().order_by('-date_updated')
            else:
                #only posts I have not yet seen
                posts = AnnouncementPost.objects.filter(is_approved=True).exclude(viewed_by__in=[user.id]).order_by('-date_updated')
        else:
            # get only approved posts
            posts = AnnouncementPost.objects.filter(is_approved=True).order_by('-date_updated')
        return get_paginated_results(posts, page)
    except Exception as err:
        print(str(err))
        return None
    
def get_author_announcements(request, author, page=1):
    try:
        if author.is_super_editor:
            posts = AnnouncementPost.objects.filter(author=author).order_by('-date_updated')
            return get_paginated_results(posts, page)
        else:
            return None
    except Exception as err:
        print(str(err))
        return None