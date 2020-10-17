from django.db import models
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework.authtoken.models import Token



def upload_location(instance, filename):
    file_path = 'account/{user_id}/{profile_picture}'.format(
        user_id=str(instance.id), profile_picture=filename)
    return file_path


class MyAccountManager(BaseUserManager):

    def create_user(self, email, display_name, username,  password=None, is_editor = False, is_super_editor = False):
        if not email:
            raise ValueError('Users must have an email address')
        if not display_name:
            raise ValueError('Users must have a name')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            display_name=display_name,
            username=username,
            is_editor = is_editor,
            is_super_editor = is_super_editor
        )

        if is_editor or is_super_editor:
            user.is_staff = True

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, display_name, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            display_name=display_name,
            username=username,
            password=password,
            is_editor=True,
            is_super_editor = True,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):

    # custom
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    display_name = models.CharField(verbose_name="name", max_length=120)
    username = models.CharField(max_length=36, unique=True)
    is_editor = models.BooleanField(default=False)
    is_super_editor = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to=upload_location, blank=True, null=True)
    # required
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['display_name', 'username']

  
    # set the manage defined above
    objects = MyAccountManager()


    def __str__(self):
        return self.display_name

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

@receiver(post_delete, sender=Account)
def submission_delete(sender, instance, **kwargs):
    try:
        Token.objects.delete(user=instance)
        if instance.profile_picture: 
            instance.profile_picture.delete(False)
    except Exception as err:
        print(err)

def compress_image(image):
        if not image:
            return None
        im = Image.open(image)
        out = BytesIO()
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGB")
        im.save(out, 'JPEG', quality=30)
        compressed = File(out, name=image.name)
        im.close()
        return compressed

def pre_save_account_post_receiver(sender, instance, *args, **kwargs):
    try:
        account_obj = Account.objects.get(pk=instance.pk)
    except Account.DoesNotExist:
        # the object does not exists, so compress the image
        if instance.profile_picture: 
            instance.profile_picture = compress_image(instance.profile_picture)
    else:
        # the object exists, so check if the image field is updated
        if account_obj.profile_picture != instance.profile_picture:
            instance.profile_picture = compress_image(instance.profile_picture)

pre_save.connect(pre_save_account_post_receiver, sender=Account)

def post_save_account_receiver(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


post_save.connect(post_save_account_receiver, sender=settings.AUTH_USER_MODEL)


'''UNCOMMENT IF YOU HAVE CREATED USERS BEFORE SETTING UP TOKENS
allUsers  = Account.objects.all()
for user in allUsers:
    Token.objects.create(user=user) '''