import os
from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from Earth.models import Article


class ArticleFrom(forms.ModelForm):
    # title = forms.CharField(max_length=30, min_length=5)
    # brief = forms.CharField(max_length=50, min_length=5)
    # head_img = forms.ImageField
    # content = forms.CharField(min_length=10)

    class Meta:
        model = Article
        fields = ('title', 'brief', 'head_img', 'content',)
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }

def handle_uploaded_file(request, f):
    print('-->', f.name)
    base_img_upload_path = 'static/imgs'
    user_path = '%s/%s' % (base_img_upload_path, request.user.userprofile.id)
    if not os.path.exists(user_path):
        os.mkdir(user_path)
    with open('%s/%s' % (user_path, f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return '/static/imgs/%s/%s' % (request.user.userprofile.id, f.name)
