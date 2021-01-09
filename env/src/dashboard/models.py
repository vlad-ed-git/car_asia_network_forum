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
from django_comments_xtd.models import XtdComment
from django.urls import reverse

def upload_location(instance, filename):
    file_path = 'announcement/{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename)
    return file_path

class AnnouncementPost(models.Model):
    title = models.CharField(max_length=220, null=False, blank=False)
    body = models.TextField(max_length=60000, null=False, blank=False)
    featured_image = models.ImageField(
        upload_to=upload_location, null=True, blank=True)
    extra_image_one = models.ImageField(
        upload_to=upload_location, null=True, blank=True)
    extra_image_two = models.ImageField(
        upload_to=upload_location, null=True, blank=True)
    extra_image_three = models.ImageField(
        upload_to=upload_location, null=True, blank=True)
    date_published = models.DateTimeField(
        auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="date updated")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=True)
    slug = models.SlugField(blank=True, unique=True)
    viewed_by = models.ManyToManyField(Account, related_name='announcement_post_viewed_by')
   
    def __str__(self):
        return self.title

    def total_viewed_by(self):
        return self.viewed_by.count()

    def get_absolute_url(self):
        return reverse('announcement_details',kwargs={'slug': self.slug})

@receiver(post_delete, sender=AnnouncementPost)
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
        msg = str(err)  +  ": announcement | announcement submission_delete"
       

def compress_image(image):
    im = Image.open(image)
    out = BytesIO()
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    im.save(out, 'JPEG', quality=70)
    compressed = File(out, name=image.name)
    im.close()
    return compressed


def pre_save_announcement_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(
            str(instance.author.id) + "-" + instance.title[0:48] )
    try:
        post_obj = AnnouncementPost.objects.get(pk=instance.pk)

        # the object exists, so check if the image field is updated
        if post_obj.featured_image != instance.featured_image:
            instance.featured_image = compress_image(instance.featured_image)

        if post_obj.extra_image_one != instance.extra_image_one:
            instance.extra_image_one = compress_image(instance.extra_image_one)

        if post_obj.extra_image_two != instance.extra_image_two:
            instance.extra_image_two = compress_image(instance.extra_image_two)

        if post_obj.extra_image_three != instance.extra_image_three:
            instance.extra_image_three = compress_image(instance.extra_image_three)

    except AnnouncementPost.DoesNotExist:
        # the object does not exists, so compress the image
        if instance.featured_image:
            instance.featured_image = compress_image(instance.featured_image)
        if instance.extra_image_one:
            instance.extra_image_one = compress_image(instance.extra_image_one)
        if instance.extra_image_two:
            instance.extra_image_two = compress_image(instance.extra_image_two)
        if instance.extra_image_three:
            instance.extra_image_three = compress_image(
                instance.extra_image_three)


pre_save.connect(pre_save_announcement_post_receiver, sender=AnnouncementPost)