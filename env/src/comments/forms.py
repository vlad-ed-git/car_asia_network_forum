from django import forms
from .models import CommentsPost


class CreateCommentsPostForm(forms.ModelForm):

    class Meta:
        model = CommentsPost
        fields = [ 'body', 'for_post_id', 'is_response_to_topic', 'is_response_to_comment', 'is_approved']

class UpdateCommentsPostForm(forms.ModelForm):
    class Meta:
        model = CommentsPost
        fields = ['body', 'for_post_id', 'is_response_to_topic', 'is_response_to_comment', 'is_approved' ]

    def save(self, commit=True):
        #override save so that only these fields are updated
        comments_post = self.instance
        comments_post.title = self.cleaned_data['title']
        topic_post.is_response_to_topic  = self.cleaned_data['is_response_to_topic']
        topic_post.is_response_to_comment   = self.cleaned_data['is_response_to_comment']
        topic_post.is_approved = self.cleaned_data['is_approved']
        
        if commit:
            comments_post.save()

        return comments_post
