from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateAnnouncementPostForm, UpdateAnnouncementPostForm
from account.models import Account
from .models import AnnouncementPost
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from topic.views import  get_context_with_side_bar
from .search_views import get_author_announcements, get_all_announcements

# Create your views here.
def announcements_view(request, author_id=None, page=1):
    context = {}
    if author_id:
        author = get_object_or_404(Account, id=author_id)
        context['posts_by_author'] = author_id
        context['posts'] = get_author_announcements(request, author=author, page=page)
    else:
        context['posts']  = get_all_announcements(request, page)
    return render(request, 'topic/dashboard/announcements.html', context)

def announcement_details_view(request, slug):
    context =  get_context_with_side_bar(request)
    post = get_object_or_404(AnnouncementPost, slug=slug)
    context['post'] = post
    if request.user.is_authenticated:
        user = request.user
        post.viewed_by.add(user)
        if user.is_super_editor:
            context['can_edit'] = True
    return render(request, 'topic/dashboard/announcement_page.html', context)


############## CRUD #################
def delete_announcement_view(request, slug, confirmed=0):
    context = {}
    user = request.user
    if not user.is_authenticated or not request.user.is_super_editor:
        return redirect('must_authenticate')

    announcement_post = get_object_or_404(AnnouncementPost, slug=slug)
    if announcement_post.author != user and not user.is_editor:
        return HttpResponse("You are not the author of that post")
    if confirmed == 0:
       #need to confirm
       context['post'] = announcement_post
       return render(request, 'topic/dashboard/editor_pages/delete.html', context)
    elif confirmed == 1: 
       context['deleted'] = True  
       announcement_post.delete()
       return render(request, 'topic/dashboard/editor_pages/delete.html', context)
    else:
        return redirect('home')
        
    
def create_announcement_view(request):
    context = {}
    user = request.user
    if not user.is_authenticated or  not request.user.is_super_editor:
        return redirect('must_authenticate')
    form = CreateAnnouncementPostForm(request.POST or None, request.FILES or None )
    if request.POST:
        if form.is_valid():
            # we need to set the author property before we can save
            obj = form.save(commit=False)
            author = Account.objects.get(email=user.email)
            obj.author = author
            obj.save()
            context['success'] = True
            form = CreateAnnouncementPostForm()
            return redirect('announcement_details', slug = obj.slug)
        else:
            context['failed'] = True
            form.initial={"title": request.POST.get("title"),  "body":  request.POST.get("body"),  "is_approved" :request.POST.get("is_approved") }
    context['create_form'] = form
    return render(request, 'topic/dashboard/editor_pages/forms/create_announcement.html', context)

def edit_announcement_view(request, slug):
    context = {}
    user = request.user
    if not user.is_authenticated or not request.user.is_super_editor:
        return redirect('must_authenticate')

    announcement_post = get_object_or_404(AnnouncementPost, slug=slug)
    if announcement_post.author != user and not user.is_editor:
        return HttpResponse("You are not the author of that post")
    if request.POST:
        form = UpdateAnnouncementPostForm(request.POST or None, request.FILES or None, instance=announcement_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success'] = True
            announcement_post = obj
            return redirect('announcement_details', slug = announcement_post.slug)
        else:
            context['failed'] = True
            form.initial={"title": request.POST.get("title"),  "body":  request.POST.get("body") , "featured_image" : announcement_post.featured_image, "extra_image_one" : announcement_post.extra_image_one, "extra_image_two" : announcement_post.extra_image_two, "extra_image_three" : announcement_post.extra_image_three, "is_approved" : announcement_post.is_approved }

    form = UpdateAnnouncementPostForm(
                            initial={
                            "title": announcement_post.title,
                            "body": announcement_post.body,
                            "featured_image" : announcement_post.featured_image,
                            "extra_image_one" : announcement_post.extra_image_one,
                            "extra_image_two" : announcement_post.extra_image_two,
                            "extra_image_three" : announcement_post.extra_image_three,
                            "is_approved" : announcement_post.is_approved
                            })
    context['update_form'] = form
    context['post'] = announcement_post
    return render(request, 'topic/dashboard/editor_pages/forms/update_announcement.html', context)




