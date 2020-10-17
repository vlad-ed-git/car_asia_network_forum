import os
from rest_framework import serializers
from blog.models import BlogPost


def validate_image_url(image = None):
    if image:
        new_url = image.url
        if "?" in new_url:
            new_url = image.url[:image.url.rfind("?")]
        return new_url
    else:
        return None

class BlogPostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')
    featured_image = serializers.SerializerMethodField('validate_featured_image_url')
    extra_image_one = serializers.SerializerMethodField('validate_extra_image_one_url')
    extra_image_two = serializers.SerializerMethodField('validate_extra_image_two_url')
    extra_image_three = serializers.SerializerMethodField('validate_extra_image_three_url')
    likes = serializers.SerializerMethodField('get_likes')
    dislikes = serializers.SerializerMethodField('get_dislikes')

    class Meta:
        model = BlogPost
        fields = ['pk', 'slug', 'title', 'body', 'featured_image', 'extra_image_one', 'extra_image_two',
                  'extra_image_three', 'likes', 'dislikes', 'views', 'date_updated', 'username']

    def get_username_from_author(self, blog_post):
        username = blog_post.author.username
        return username

    def get_likes(self, blog_post):
        return blog_post.total_likes()

    def get_dislikes(self, blog_post):
        return blog_post.total_dislikes()

    def validate_featured_image_url(self, blog_post):
        return validate_image_url(image = blog_post.featured_image)

    def validate_extra_image_one_url(self, blog_post):
        return validate_image_url(image = blog_post.extra_image_one)

    def validate_extra_image_two_url(self, blog_post):
        return validate_image_url(image = blog_post.extra_image_two)

    def validate_extra_image_three_url(self, blog_post):
        return validate_image_url(image = blog_post.extra_image_three)



class BlogPostUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'featured_image', 'extra_image_one', 'extra_image_two',
                  'extra_image_three',]


class BlogPostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'featured_image', 'extra_image_one', 'extra_image_two',
                  'extra_image_three', 'author']

    def save(self):
        featured_image = None
        extra_image_one = None
        extra_image_two = None
        extra_image_three = None
        try:
            if self.validated_data['featured_image']:
                featured_image = self.validated_data['featured_image']
            if self.validated_data['extra_image_one']:
                extra_image_one = self.validated_data['extra_image_one']
            if self.validated_data['extra_image_two']:
                extra_image_two = self.validated_data['extra_image_two']
            if self.validated_data['extra_image_three']:
                extra_image_three = self.validated_data['extra_image_three']
        except KeyError as err:
            #ignore -- some image(s) is not set
            print(str(err))
        try:
            title = self.validated_data['title']
            body = self.validated_data['body']
            blog_post = BlogPost(
                author=self.validated_data['author'],
                title=title,
                body=body,
                featured_image=featured_image,
                extra_image_one=extra_image_one,
                extra_image_two=extra_image_two,
                extra_image_three=extra_image_three
                )

            blog_post.save()
            return blog_post
        except KeyError as err:
            print(str(err))
            raise serializers.ValidationError(
                {"response": "You must have a title, some content."})
