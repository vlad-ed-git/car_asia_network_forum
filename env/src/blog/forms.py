from django import forms
from .models import BlogPost


class CreateBlogPostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'featured_image',
                  'extra_image_one', 'extra_image_two', 'extra_image_three']

class UpdateBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'featured_image',
                  'extra_image_one', 'extra_image_two', 'extra_image_three']

    def save(self, commit=True):
        #override save so that only these fields are updated
        blog_post = self.instance
        blog_post.title = self.cleaned_data['title']
        blog_post.body = self.cleaned_data['body']

        #update image is a new one has been provided
        if self.cleaned_data['featured_image']:
            blog_post.featured_image = self.cleaned_data['featured_image']

        if self.cleaned_data['extra_image_one']:
            blog_post.extra_image_one = self.cleaned_data['extra_image_one']

        if self.cleaned_data['extra_image_two']:
            blog_post.extra_image_two = self.cleaned_data['extra_image_two']

        if self.cleaned_data['extra_image_three']:
            blog_post.extra_image_three = self.cleaned_data['extra_image_three']

        if commit:
            blog_post.save()

        return blog_post
