from django.shortcuts import render
from .models import AchievementPost
from forum_analytics.models import LogKey, LogType
from forum_analytics.views import saveAnalytics

# Create your views here.
def get_achievements(request):
    choices  = AchievementPost._meta.get_field('category').choices
    return choices

def add_achievement(achievement, level, request = None, userWithAchievement = None, ):
    try:
        if request:
            user = request.user
        else:
            user = userWithAchievement
        achievement = AchievementPost(user = user, achievement = achievement, level = level)
        achievement.save()
    except Exception as err:
        msg = str(err) + "  : achievements | add_achievement"
        saveAnalytics(request =None, log_type=LogType.ERROR, log_key=LogKey.EXCEPTION_RAISED, log_value=msg, resolved=False)

def get_new_user_achievements_count(request):
    try:
        user_achievements_count = AchievementPost.objects.filter(user=request.user, viewed_by_user=False).count()
        if user_achievements_count > 0:
            return user_achievements_count
        else:
            return None
    except Exception as err:
        msg = str(err) + ": achievements | get_new_user_achievements_count" 
        saveAnalytics(request =None, log_type=LogType.ERROR, log_key=LogKey.EXCEPTION_RAISED, log_value=msg, resolved=False)
        return None

def get_new_user_achievements(request):
    try:
        found_achievements = []
        new_achievements = AchievementPost.objects.filter(user=request.user, viewed_by_user=False)
        for new_achievement in new_achievements:
            found_achievements.append(new_achievement)
        return found_achievements
    except Exception as err:
        msg = str(err) + ": achievements | get_new_user_achievements"
        saveAnalytics(request =None, og_type=LogType.ERROR, log_key=LogKey.EXCEPTION_RAISED, log_value=msg, resolved=False)
        return None

def mark_new_user_achievements_as_viewed(request):
    try:
        AchievementPost.objects.filter(user=request.user).update(viewed_by_user=True)
    except Exception as err:
        msg = str(err) + ": achievements | mark_new_user_achievements_as_viewed"
        saveAnalytics(request =None, og_type=LogType.ERROR, log_key=LogKey.EXCEPTION_RAISED, log_value=msg, resolved=False)

def get_all_user_achievements(request):
    try:
        discussion_starter = AchievementPost.objects.filter(user=request.user, achievement='DS').count()
        got_likes = AchievementPost.objects.filter(user=request.user, achievement='TU').count()
        celebrity = AchievementPost.objects.filter(user=request.user, achievement='CEL').count()
        avid_reader = AchievementPost.objects.filter(user=request.user, achievement='RE').count()
        return {'discussion_starter' : discussion_starter, 'got_likes' : got_likes, 'celebrity' : celebrity, 'avid_reader' : avid_reader}
    except Exception as err:
        msg = str(err) + ": achievements | get_all_user_achievements" 
        saveAnalytics(request =None, og_type=LogType.ERROR, log_key=LogKey.EXCEPTION_RAISED, log_value=msg, resolved=False)
        return None
