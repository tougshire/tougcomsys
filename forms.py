from django import forms

from tougcomsys.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'article',
            'in_reply_to',
            'comment_text',
        ]

