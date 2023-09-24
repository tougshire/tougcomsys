from django.urls import reverse_lazy
from django import forms
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from tougcomsys.models import Article, ArticleEventdate, ArticlePlacement, Comment, Image
from touglates.widgets import TouglateDateInput

def validate_blank(value):
    if value=='':
        return
    else:
        raise ValidationError(
            _("%(value)s failed"),
            params={"value": value},
        )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'article',
            'in_reply_to',
            'comment_text',
        ]

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "headline",
            "subheadline",
            "content_format",
            "content",
            "hashtags",
            "list_image",
            "list_image_location",
            "detail_image",
            "detail_image_location",
            "featured_image",
            "summary_format",
            "summary",
            "readmore",
            "author",
            "descriptive_date",
            "show_author",
            "show_updated",
            "sortable_date",
            "sticky",
            "draft_status",
            "allow_comments",
            "slug",
        ]
        widgets = {
            'headline':forms.TextInput(attrs={'class':'width_050'}),
            'subheadline':forms.TextInput(attrs={'class':'width_050'}),
            'content':forms.Textarea(attrs={'class':'width_050'}),
            'summary':forms.Textarea(attrs={'class':'width_050'}),
            'sortable_date':TouglateDateInput()
        }

class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = [
            "title",
            "author",
            "file",
            "alt_text",
            "url",
        ]

class ArticleArticleEventDateForm(forms.ModelForm):
    class Meta:
        model = ArticleEventdate
        fields = [
            'article',
            'whendate',
            'whentime',
            'timelen',
        ]
        widgets = {
            'whendate': TouglateDateInput()
        }

class ArticlePlacementForm(forms.ModelForm):
    class Meta:
        model = ArticlePlacement
        fields = [
            'article',
            'placement',
            'expiration_date',
        ]
        widgets = {
            'expiration_date': TouglateDateInput()
        }

ArticleArticleEventDateFormSet = forms.inlineformset_factory(Article, ArticleEventdate, form=ArticleArticleEventDateForm, extra=1, can_delete=True)
ArticlePlacementFormSet = forms.inlineformset_factory(Article, ArticlePlacement, form=ArticlePlacementForm, extra=1, can_delete=True)