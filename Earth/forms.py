import os
from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from Earth.models import Article,Category


class ArticleFrom(forms.ModelForm):
    # title = forms.CharField(max_length=30, min_length=5)
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','width':'900px'}))
    brief = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # head_img = forms.ImageField
    # content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','value':'{{ new_article.content|safe }}'}))
    content = forms.CharField()

    class Meta:
        model = Article
        fields = ('title', 'brief', 'head_img', 'content')
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }
class CategoryFrom(forms.ModelForm):
    name = forms.CharField(min_length=1,max_length=30)
    class Meta:
        model = Category
        fields = ('id','name')
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
