from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from Earth import models, forms
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from Earth.forms import ArticleFrom, handle_uploaded_file


def acc_login(request):
    '''
    登录,如果没有登录就先登录
    :param request:
    :return:
    '''
    if request.method == 'POST':
        print(request.POST)
        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user is not None:
            # pass authentication
            login(request, user)
            return HttpResponseRedirect(request.GET.get('next') or '/blog')
        else:
            login_err = "Wrong username or password!"
            print('---else request-->', request)
            return render(request, 'login.html', {'login_err': login_err})
    return render(request, 'login.html')
def acc_logout(request):
    '''
    退出,返回到首页
    :param request:
    :return:
    '''
    logout(request)
    return HttpResponseRedirect('/blog')


def index(request):
    #     return HttpResponse('hello')
    # # def index(request):
    # # # def post_list(request):
    '''所有已发布文章'''
    blog_all = models.Article.objects.annotate(num_comment=Count('id')).filter(published_date__isnull=False).order_by(
            '-published_date')
    # blog_all = models.Article.objects.all()
    print('---blog_all--->', blog_all)
    posts = pages(request, blog_all)
    return render(request, 'blog/post_list.html', {'posts': posts, 'page': True})


def pages(request, blog_all):
    '''
    分页功能实现,根据SQL查询内容,设定分多少页,输出
    :param request:
    :param blog_all:
    :return:
    '''
    paginator = Paginator(blog_all, 8)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return posts


def post_detail(request, pk):
    post = get_object_or_404(models.Article, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def blog_new(request):
    if request.method == "POST":
        form = ArticleFrom(request.POST)
        print('这里是post的request', request)
        print('这里是post的form', form)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['author_id'] = request.user.userprofile.id
            # new_img_path = handle_uploaded_file(request,request.FILES['head_img'])
            # print('---->',form_data)
            # print('---->',new_img_path)
            # form_data['head_img'] = new_img_path
            new_article_obj = models.Article(**form_data)
            # print('----obj-->',new_article_obj.head_img)
            new_article_obj.save()
            # post = form.save(commit=False)
            print(new_article_obj)
            return redirect('Earth.views.blog_drafts')
    else:
        # form = models.Post.objects.all()
        new_article = ArticleFrom()
        # print('这里是get的form',form)
    return render(request, 'blog/blog_edit.html', {'new_article': new_article})

@login_required
def blog_publish(request, pk):
    post = get_object_or_404(models.Article, pk=pk)
    post.publish()
    return redirect('Earth.views.post_detail', pk=pk)


def post_draft_list(request):
    posts = models.Article.objects.filter(published_date__isnull=True).order_by('-created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def blog_remove(request, pk):
    post = get_object_or_404(models.Article, pk=pk)
    post.delete()
    return redirect('Earth.views.blog_list')
@login_required
def blog_admin(request):
    return render(request, 'blog/admin.html')
@login_required
def blog_list(request):
    '''
    管理后台已发布文章列表
    :param request:
    :return:
    '''
    blog_all = models.Article.objects.annotate(num_comment=Count('id')).filter(published_date__isnull=False).order_by(
            '-published_date')
    posts = pages(request, blog_all)
    return render(request, 'blog/blog_list.html', {'posts': posts, 'page': True})
@login_required
def blog_drafts(request):
    '''
    管理后台草稿箱列表
    :param request:
    :return:
    '''
    blog_all = models.Article.objects.filter(published_date__isnull=True).order_by('-created_date')
    posts = pages(request, blog_all)
    return render(request, 'blog/blog_list.html', {'posts': posts, 'page': True})
@login_required
def blog_edit(request, pk):
    post = get_object_or_404(models.Article, pk=pk)
    # print(post)
    # print(request.method,"-------->")
    if request.method == "POST":
        form = ArticleFrom(request.POST, instance=post)
        # print('---------->',form)
        # print('判断form')
        if form.is_valid():
            post = form.save(commit=False)
            # print('表单正常')
            # post.text = request.POST.get('text')
            post.author = request.user
            # print('开始保存')
            post.save()
            # return render(request,'blog/admin.html')
            # print('ok')
            '''
            保存成功后跳转到详情页
            '''
            return redirect('Earth.views.post_detail', pk=post.pk)
    else:
        new_article = ArticleFrom(instance=post)
        # print('如果是get的方式,那就先查询')
    return render(request, 'blog/blog_edit.html', {'new_article': new_article})



