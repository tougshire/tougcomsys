from django import forms
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from tougcomsys.models import Comment

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

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.CharField(validators=[EmailValidator()],required=False)
    phone = forms.CharField(max_length=15, required=False)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    gender = forms.CharField(max_length=10,required=False, validators=[validate_blank])