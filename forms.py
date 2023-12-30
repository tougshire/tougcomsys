from django.urls import reverse_lazy
from django import forms
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from tougcomsys.models import (
    Article,
    ArticleEventdate,
    ArticlePlacement,
    Comment,
    Image,
)
from touglates.widgets import TouglateDateInput, TouglateRelatedSelect


def validate_blank(value):
    if value == "":
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
            "article",
            "in_reply_to",
            "comment_text",
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
        ]

        widgets = {
            "headline": forms.TextInput(attrs={"class": "width_050"}),
            "subheadline": forms.TextInput(attrs={"class": "width_050"}),
            "content": forms.Textarea(attrs={"class": "width_050"}),
            "summary": forms.Textarea(attrs={"class": "width_050"}),
        }


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
            "allow_comments",
        ]

        widgets = {
            "headline": forms.TextInput(attrs={"class": "width_050"}),
            "subheadline": forms.TextInput(attrs={"class": "width_050"}),
            "content": forms.Textarea(attrs={"class": "width_050"}),
            "summary": forms.Textarea(attrs={"class": "width_050"}),
            "sortable_date": TouglateDateInput(),
        }


# ArticleForm for creating and ArticleFormN for updating
# ArticleForm2 includes details
class ArticleForm2(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "list_image",
            "list_image_location",
            "list_image_link",
            "detail_image",
            "detail_image_location",
            "detail_image_link",
            "featured_image",
        ]
        widgets = {
            "list_image": TouglateRelatedSelect(
                related_data={
                    "model": "Image",
                    "add_url": reverse_lazy("tougcomsys:article_image_create"),
                }
            ),
            "detail_image": TouglateRelatedSelect(
                related_data={
                    "model": "Image",
                    "add_url": reverse_lazy("tougcomsys:article_image_create"),
                }
            ),
            "featured_image": TouglateRelatedSelect(
                related_data={
                    "model": "Image",
                    "add_url": reverse_lazy("tougcomsys:article_image_create"),
                }
            ),
        }


"""
ArticleForm for creating and ArticleFormN for updating
ArticleForm3 works with ArticlePlacementFormset
"""


class ArticleForm3(forms.ModelForm):
    class Meta:
        model = Article
        fields = []


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


"""
ArticleForm for creating and ArticleFormN for updating
ArticleForm5 is for publishing the post
"""


class ArticleForm5(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["slug", "draft_status", "embeddable", "embed_headlines"]


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
            "article",
            "whendate",
            "whentime",
            "timelen",
        ]
        widgets = {"whendate": TouglateDateInput()}


class ArticlePlacementForm(forms.ModelForm):
    class Meta:
        model = ArticlePlacement
        fields = [
            "article",
            "placement",
            "expiration_date",
            "sticky",
            "sortable_date",
        ]
        widgets = {"expiration_date": TouglateDateInput()}


ArticleArticleEventDateFormSet = forms.inlineformset_factory(
    Article,
    ArticleEventdate,
    form=ArticleArticleEventDateForm,
    extra=1,
    can_delete=True,
)
ArticlePlacementFormSet = forms.inlineformset_factory(
    Article, ArticlePlacement, form=ArticlePlacementForm, extra=5, can_delete=True
)
