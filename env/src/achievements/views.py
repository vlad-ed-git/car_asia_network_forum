from django.shortcuts import render
from .models import AchievementPost

# Create your views here.
def get_achievements(request):
    choices  = AchievementPost._meta.get_field('category').choices
    return choices