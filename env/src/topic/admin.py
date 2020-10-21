from django.contrib import admin
from django_comments_xtd.admin import XtdCommentsAdmin
from topic.models import TopicPost, CustomComment


class CustomCommentAdmin(XtdCommentsAdmin):
    list_display = ('cid', 'name', 'object_pk',
                    'ip_address', 'submit_date', 'followup', 'is_public',
                    'is_removed')
    fieldsets = (
        (None, {'fields': ('content_type', 'object_pk', 'site')}),
        ('Content', {'fields': ('user', 'user_name', 'user_email',
                                'user_url', 'comment', 'followup')}),
        ('Metadata', {'fields': ('submit_date', 'ip_address',
                                 'is_public', 'is_removed')}),
    )

admin.site.register(CustomComment, CustomCommentAdmin)
admin.site.register(TopicPost)

