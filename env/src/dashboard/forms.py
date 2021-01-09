from django import forms
from .models import AnnouncementPost


class CreateAnnouncementPostForm(forms.ModelForm):

    class Meta:
        model = AnnouncementPost
        fields = ['title', 'body', 'featured_image',
                  'extra_image_one', 'extra_image_two', 'extra_image_three', 'is_approved']

class UpdateAnnouncementPostForm(forms.ModelForm):
    class Meta:
        model = AnnouncementPost
        fields = ['title', 'body',  'featured_image',
                  'extra_image_one', 'extra_image_two', 'extra_image_three', 'is_approved' ]

    def save(self, commit=True):
        #override save so that only these fields are updated
        announcement_post = self.instance
        announcement_post.title = self.cleaned_data['title']
        announcement_post.body = self.cleaned_data['body']
        announcement_post.is_approved = self.cleaned_data['is_approved']

        #update image is a new one has been provided
        if self.cleaned_data['featured_image']:
            announcement_post.featured_image = self.cleaned_data['featured_image']

        if self.cleaned_data['extra_image_one']:
            announcement_post.extra_image_one = self.cleaned_data['extra_image_one']

        if self.cleaned_data['extra_image_two']:
            announcement_post.extra_image_two = self.cleaned_data['extra_image_two']

        if self.cleaned_data['extra_image_three']:
            announcement_post.extra_image_three = self.cleaned_data['extra_image_three']

        if commit:
            announcement_post.save()

        return announcement_post
