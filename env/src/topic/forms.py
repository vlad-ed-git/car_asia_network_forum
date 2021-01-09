from django import forms
from .models import TopicPost


class CreateTopicPostForm(forms.ModelForm):

    class Meta:
        model = TopicPost
        fields = ['title', 'body', 'tags', 'featured_image',
                  'extra_image_one', 'extra_image_two', 'extra_image_three', 'category', 'is_approved']

class UpdateTopicPostForm(forms.ModelForm):
    class Meta:
        model = TopicPost
        fields = ['title', 'body', 'tags', 'featured_image',
                  'extra_image_one', 'extra_image_two', 'extra_image_three', 'category', 'is_approved' ]

    def save(self, commit=True):
        #override save so that only these fields are updated
        topic_post = self.instance
        topic_post.title = self.cleaned_data['title']
        topic_post.tags = self.cleaned_data['tags']
        topic_post.body = self.cleaned_data['body']
        topic_post.category  = self.cleaned_data['category']
        topic_post.is_approved = self.cleaned_data['is_approved']

        #update image is a new one has been provided
        if self.cleaned_data['featured_image']:
            topic_post.featured_image = self.cleaned_data['featured_image']

        if self.cleaned_data['extra_image_one']:
            topic_post.extra_image_one = self.cleaned_data['extra_image_one']

        if self.cleaned_data['extra_image_two']:
            topic_post.extra_image_two = self.cleaned_data['extra_image_two']

        if self.cleaned_data['extra_image_three']:
            topic_post.extra_image_three = self.cleaned_data['extra_image_three']

        if commit:
            topic_post.save()

        return topic_post
