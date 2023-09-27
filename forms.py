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

# "headline",
# "subheadline",
# "content_format",
# "content",
# "hashtags",
# "list_image",
# "list_image_location",
# "detail_image",
# "detail_image_location",
# "featured_image",
# "summary_format",
# "summary",
# "readmore",
# "author",
# "descriptive_date",
# "show_author",
# "show_updated",
# "sortable_date",
# "sticky",
# "draft_status",
# "allow_comments",
# "slug",
#   'sortable_date':TouglateDateInput()

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "headline",
            "subheadline",
            "content_format",
            "content",
            "hashtags",
            "summary_format",
            "summary",
            "readmore",
            "author",
            "draft_status",
            "slug",
        ]

        widgets = {
            'headline':forms.TextInput(attrs={'class':'width_050'}),
            'subheadline':forms.TextInput(attrs={'class':'width_050'}),
            'content':forms.Textarea(attrs={'class':'width_050'}),
            'summary':forms.Textarea(attrs={'class':'width_050'}),
        }

# 1 "headline",
# 1 "subheadline",
# 1 "content_format",
# 1 "content",
# 1 "hashtags",
# 2 "list_image",
# 2 "list_image_location",
# 2 "detail_image",
# 2 "detail_image_location",
# 2 "featured_image",
# 1 "summary_format",
# 1 "summary",
# 1 "readmore",
# 1 "author",
# 4 "descriptive_date",
# 3 "show_author",
# 3 "show_updated",
# 4 "sortable_date",
# 3 "sticky",
# 1 "draft_status",
# 3 "allow_comments",
# 1 "slug",
#   'sortable_date':TouglateDateInput()


# ArticleForm for creating and ArticleFormN for updating
# ArticleForm1 is mostly the same as ArticleForm, but also had slug

class ArticleForm1(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "headline",
            "subheadline",
            "content_format",
            "content",
            "hashtags",
            "summary_format",
            "summary",
            "readmore",
            "author",
            "draft_status",
            "allow_comments",

        ]

        widgets = {
            'headline':forms.TextInput(attrs={'class':'width_050'}),
            'subheadline':forms.TextInput(attrs={'class':'width_050'}),
            'content':forms.Textarea(attrs={'class':'width_050'}),
            'summary':forms.Textarea(attrs={'class':'width_050'}),
            'sortable_date':TouglateDateInput()
        }

# ArticleForm for creating and ArticleFormN for updating
# ArticleForm2 includes details
class ArticleForm2(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "list_image",
            "list_image_location",
            "detail_image",
            "detail_image_location",
            "featured_image",
        ]


"""
ArticleForm for creating and ArticleFormN for updating
ArticleForm3 works with ArticlePlacementFormset
"""
class ArticleForm3(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
        ]
"""
ArticleForm for creating and ArticleFormN for updating
ArticleForm4 works with ArticleArticleEventDateFormset
"""
class ArticleForm4(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "descriptive_date",
        ]

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
            "sticky",
            'sortable_date',

        ]
        widgets = {
            'expiration_date': TouglateDateInput()
        }

ArticleArticleEventDateFormSet = forms.inlineformset_factory(Article, ArticleEventdate, form=ArticleArticleEventDateForm, extra=1, can_delete=True)
ArticlePlacementFormSet = forms.inlineformset_factory(Article, ArticlePlacement, form=ArticlePlacementForm, extra=1, can_delete=True)
