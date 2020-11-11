from django.shortcuts import render, redirect
from topic.views import increment_view_count, search_topics, get_topic_post_or_404, get_all_topics, get_most_liked_topics, get_top_viewed_topics, like_topic_post, dislike_topic_post,user_dislikes_topic_post, user_likes_topic_post, user_owns_topic_post, get_all_topics_by_author, get_topic_categories, get_all_topics_by_category
from django.conf import settings

# home page
def home_view(request, posts_by_author = None, post_type = None, category = None ):
    context = {}
    filter_by_query = ""
    page = request.GET.get('page', 1)
    if request.GET:
        #displaying search results
        filter_by_query =  request.GET.get('query','')
        post_type  = request.GET['post_type'] 
        context['query'] = str(filter_by_query)
        context['post_type'] = str(post_type)
        context['topic_posts'] = search_topics(query=filter_by_query, page=page)
    else:
        if post_type == None:
            context['post_type'] = 'topic' #default post type
        else:
            context['post_type'] =  post_type
        if context['post_type'] == 'topic':
            if posts_by_author != None:
                context['topic_posts'] = get_all_topics_by_author(request, page=page, username=posts_by_author)
            elif category != None:
                context['topic_posts'] = get_all_topics_by_category(request, page=page, category=category)
            else:
                context['topic_posts'] = get_all_topics(request, page=page)
    context['most_viewed_topics'] = get_top_viewed_topics()
    context['popular_topics'] = get_most_liked_topics()
    context['show_search_bar'] = True
    context['topic_categories'] = get_topic_categories(request)
    return render(request, 'website/home.html', context)



def post_details_view(request, post_type, slug):
    if post_type == 'topic':
       topic = get_topic_post_or_404(slug=slug)
       increment_view_count(topic.slug)


    context = {}
    if request.user.is_authenticated:
        user = request.user
        context['user_dislikes_post'] = user_dislikes_topic_post(user=user, topic=topic)
        context['user_likes_post'] = user_likes_topic_post(user=user, topic=topic)
        context['is_my_post'] = user_owns_topic_post(user=user, topic=topic)

    context['post'] = topic
    context['post_type'] = post_type
    return render(request, 'website/post_page.html', context)

def like_post_view(request, post_type, slug):
    if post_type == 'topic':
        like_topic_post(user=request.user, slug=slug)
    return redirect('post_details', post_type=post_type, slug=slug)

def dislike_post_view(request, post_type, slug):
    if post_type == 'topic':
        dislike_topic_post(user=request.user, slug=slug)
    return redirect('post_details', post_type=post_type, slug=slug)

def handler404(request, exception):
    return render(request, 'website/error_pages/404.html', status=404)

def handler500(request):
    return render(request, 'website/error_pages/500.html', status=500)