from django.db import models
from django.utils.text import slugify
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from account.models import Account
from django.utils.translation import gettext_lazy as _


class CommentsPost(models.Model):
    body = models.TextField(max_length=5000, null=False, blank=False)
    for_post_id = models.IntegerField(blank=False, null=False)
    is_response_to_topic = models.BooleanField(default=False)
    is_response_to_comment = models.BooleanField(default=False)
    date_published = models.DateTimeField(
        auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="date updated")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    slug = models.SlugField(blank=True, unique=True)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(Account, related_name='comments_post_likes')
    dislikes = models.ManyToManyField(Account, related_name='comments_post_dislikes')

    def __str__(self):
        return self.slug

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()


@receiver(post_delete, sender=CommentsPost)
def submission_delete(sender, instance, **kwargs):
    try:
        if instance.featured_image:
            instance.featured_image.delete(False)
        if instance.extra_image_one:
            instance.extra_image_one.delete(False)
        if instance.extra_image_two:
            instance.extra_image_two.delete(False)
        if instance.extra_image_three:
            instance.extra_image_three.delete(False)
    except Exception as err:
        print(err)


def pre_save_comments_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(
            instance.author.username + "-" + str(instance.for_post_id) + "-" + instance.body[0:48])

pre_save.connect(pre_save_comments_post_receiver, sender=CommentsPost)

