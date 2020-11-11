from django.contrib import admin
from django_comments_xtd.admin import XtdCommentsAdmin
from achievements.models import AchievementPost

admin.site.register(AchievementPost)

