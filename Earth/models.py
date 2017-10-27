from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime
import django



class Tag(models.Model):
    class Meta:
        app_label = 'Earth'
        verbose_name = '标签'
        verbose_name_plural = '标签'

    name = models.CharField(max_length=40,unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        app_label = 'Earth'
        verbose_name = '分类目录'
        verbose_name_plural = '分类目录'

    name = models.CharField(max_length=40,unique=True)
    alias = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Article(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=200,unique=True)
    brief = models.CharField(null=True, blank=True, max_length=255)
    content = models.TextField(u"文章内容")
    md = models.TextField(u"文章内容",default='')
    tags = models.ForeignKey(Tag)
    # 分类目录
    category = models.ForeignKey(Category)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    head_img = models.ImageField(u"文章标题图片", upload_to="uploads", blank=True, null=True)
    status_choices = (('draft', u"草稿"),
                      ('published', u"已发布"),
                      ('hidden', u"隐藏"),
                      )
    status = models.CharField(choices=status_choices, default='published', max_length=32)
    copyright = models.TextField(default='Medivh')
    reprinted = models.CharField(default='http://www.mknight.cn',max_length=64)
    views = models.IntegerField(default='0')
    def publish(self):
        # self.published_date = timezone.now()
        self.published_date = datetime.now().strftime("%Y-%m-%d %H:%I:%S")
        self.save()

    def __str__(self):
        return self.title
class About(models.Model):
    content = models.TextField(u"关于作者")
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    signature = models.CharField(max_length=255, blank=True, null=True)
    head_img = models.ImageField(height_field=150, width_field=150, blank=True, null=True)

    # head_img = models.ImageField(blank=True,null=True,upload_to='uploads')
    # head_img = models.ImageField(blank=True,null=True)
    # friends = models.ManyToManyField('self',related_name='my_friends',blank=True)
    def __str__(self):
        return self.name
