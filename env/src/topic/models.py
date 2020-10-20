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

def upload_location(instance, filename):
    file_path = 'topic/{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename)
    return file_path

class TopicPost(models.Model):
    class CATEGORIES(models.TextChoices):
        CA ='CA', _('Car Accessories')
        CP = 'CP', _('Car Performance Parts')
        CC = 'CC', _('Continental Cars')
        CEI = 'CEI', _('Cosmetic Enhancement Items')
        GCD = 'GCD', _('General Car Discussion')
        ICE = 'ICE', _('In Car Entertainment')
        JC = 'JC', _('Japanese Cars')
        MR = 'MR', _('Maintenance & Repairs')
        TR = 'TR', _('Tyres & Rims')
        OTHER = 'O', _('NON CAR-RELATED')

    title = models.CharField(max_length=200, null=False, blank=False)
    body = models.TextField(max_length=5000, null=False, blank=False)
    category = models.CharField(max_length=5, choices=CATEGORIES.choices, default=CATEGORIES.OTHER, null=False, blank=False)
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
    is_approved = models.BooleanField(default=False)
    slug = models.SlugField(blank=True, unique=True)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(Account, related_name='topic_post_likes')
    dislikes = models.ManyToManyField(Account, related_name='topic_post_dislikes')

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()


@receiver(post_delete, sender=TopicPost)
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


def compress_image(image):
    im = Image.open(image)
    out = BytesIO()
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    im.save(out, 'JPEG', quality=30)
    compressed = File(out, name=image.name)
    im.close()
    return compressed


def pre_save_topic_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(
            instance.author.username + "-" + instance.title[0:48] )
    try:
        post_obj = TopicPost.objects.get(pk=instance.pk)

        # the object exists, so check if the image field is updated
        if post_obj.featured_image != instance.featured_image:
            instance.featured_image = compress_image(instance.featured_image)

        if post_obj.extra_image_one != instance.extra_image_one:
            instance.extra_image_one = compress_image(instance.extra_image_one)

        if post_obj.extra_image_two != instance.extra_image_two:
            instance.extra_image_two = compress_image(instance.extra_image_two)

        if post_obj.extra_image_three != instance.extra_image_three:
            instance.extra_image_three = compress_image(instance.extra_image_three)

    except TopicPost.DoesNotExist:
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


pre_save.connect(pre_save_topic_post_receiver, sender=TopicPost)
