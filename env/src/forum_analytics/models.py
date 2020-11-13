from django.db import models
from account.models import Account
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.
class ForumAnalytics(models.Model):
    class TYPE(models.TextChoices):
        DEBUG = 'D', _('DEBUG')
        ERROR = 'E', _('ERROR')
        INFO = 'I', _('INFO')
    log_key = models.CharField(max_length=200, null=False, blank=False)
    log_value = models.TextField(max_length=5000, null=False, blank=False)
    log_type = models.CharField(max_length=1, choices=TYPE.choices, default=TYPE.INFO, null=False, blank=False)
    date_logged = models.DateTimeField(auto_now_add=True, verbose_name="date logged")
    resolved = models.BooleanField(default=True, null=False, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=False, default=None)
    ip_address = models.GenericIPAddressField(null=True)

    def __str__(self):
        return "Forum Analytics"