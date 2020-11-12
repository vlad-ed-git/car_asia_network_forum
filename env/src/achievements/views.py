from django.shortcuts import render
from .models import AchievementPost

# Create your views here.
def get_achievements(request):
    choices  = AchievementPost._meta.get_field('category').choices
    return choices

def add_achievement(request, achievement, level):
    try:
        achievement = AchievementPost(user = request.user, achievement = achievement, level = level)
        achievement.save()
    except Exception as err:
        print(err)

def get_new_user_achievements_count(request):
    try:
        user_achievements_count = AchievementPost.objects.filter(user=request.user, viewed_by_user=False).count()
        if user_achievements_count > 0:
            return user_achievements_count
        else:
            return None
    except Exception as err:
        print(err)
        return None

def get_new_user_achievements(request):
    try:
        new_achievements = AchievementPost.objects.filter(user=request.user, viewed_by_user=False)
        return new_achievements
    except Exception as err:
        print(err)
        return None

def mark_new_user_achievements_as_viewed(request):
    try:
        AchievementPost.objects.filter(user=request.user).update(viewed_by_user=True)
    except Exception as err:
        print(err)

def get_all_user_achievements(request):
    try:
        discussion_starter = AchievementPost.objects.filter(user=request.user, achievement='DS').count()
        got_likes = AchievementPost.objects.filter(user=request.user, achievement='TU').count()
        celebrity = AchievementPost.objects.filter(user=request.user, achievement='CEL').count()
        avid_reader = AchievementPost.objects.filter(user=request.user, achievement='RE').count()
        return {'discussion_starter' : discussion_starter, 'got_likes' : got_likes, 'celebrity' : celebrity, 'avid_reader' : avid_reader}
    except Exception as err:
        print(err)
        return None
