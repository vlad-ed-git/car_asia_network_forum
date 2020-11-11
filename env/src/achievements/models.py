from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from account.models import Account
from django.utils.translation import gettext_lazy as _

class AchievementPost(models.Model):
    class CATEGORIES(models.TextChoices):
        RE = 'RE', _('Avid Reader')
        DS ='DS', _('Discussion Starter')
        CEL = 'CEL', _('Celebrity')
        TU = 'TU', _('Thumbs Up')
        NEWBIE = 'NM', _('NEW MEMBER')
    achievement = models.CharField(max_length=6, choices=CATEGORIES.choices, default=CATEGORIES.NEWBIE, null=False, blank=False)
    level = models.PositiveIntegerField(null=False, blank=False)
    viewed_by_user = models.BooleanField(default=False)
    slug = models.SlugField(blank=True, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.achievement

    def total_likes(self):
        return self.likes.count()

def pre_save_achievement_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(
            instance.user.username + "-" + instance.achievement[0:48] )

pre_save.connect(pre_save_achievement_post_receiver, sender=AchievementPost)