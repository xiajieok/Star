from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from Earth import models, forms
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from Earth.forms import ArticleFrom, handle_uploaded_file, CategoryFrom, AboutFrom
from django.http import Http404


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
    posts = pages(request, blog_all)
    about_obj = models.About.objects.filter(id=1)
    return render(request, 'blog/post_list.html', {'posts': posts, 'page': True, 'about_obj': about_obj})


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
    about_obj = models.About.objects.filter(id=1)
    return render(request, 'blog/post_detail.html', {'post': post, 'is_post': True, 'about_obj': about_obj})


@login_required
def blog_new(request):
    if request.method == "POST":
        form = ArticleFrom(request.POST)
        print('这里是post的request', request.POST)
        # print('这里是post的form', form)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['author_id'] = request.user.userprofile.id
            # print('ID--->',request.POST.get('category_id'))
            form_data['category_id'] = request.POST.get('category_id')
            # 不知道咋回事,反正就是category_id必须手动加进去
            print('--->form_data', form_data)
            # form_data['category_id'] = request.user.userprofile.id
            # new_img_path = handle_uploaded_file(request,request.FILES['head_img'])
            # print('---->',form_data)
            # print('---->',new_img_path)
            # form_data['head_img'] = new_img_path
            new_article_obj = models.Article(**form_data)
            # print('----obj-->',new_article_obj.category_id)
            new_article_obj.save()
            # post = form.save(commit=False)
            print(new_article_obj)
            return redirect('Earth.views.blog_drafts')
    else:
        # form = models.Post.objects.all()
        new_article = ArticleFrom()
        category_list = models.Category.objects.all()
        # print('这里是get的form',form)
    return render(request, 'blog/blog_edit.html',
                  {'new_article': new_article, 'category_list': category_list, 'is_new': True})


@login_required
def blog_publish(request, pk):
    post = get_object_or_404(models.Article, pk=pk)
    post.publish()
    # return redirect('Earth.views.post_detail', pk=pk)
    blog_all = models.Article.objects.filter(published_date__isnull=True).order_by('-created_date')
    posts = pages(request, blog_all)
    return render(request, 'blog/table.html', {'posts': posts})


@login_required
def blog_remove(request, pk):
    post = get_object_or_404(models.Article, pk=pk)
    post.delete()
    blog_all = models.Article.objects.annotate(num_comment=Count('id')).filter(published_date__isnull=False).order_by(
            '-published_date')
    posts = pages(request, blog_all)
    return render(request, 'blog/table.html', {'posts': posts})


@login_required
def blog_admin(request):
    return render(request, 'blog/blog_list.html')


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
    return render(request, 'blog/blog_list.html', {'posts': posts, 'page': True, 'is_list': True})


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
        edit_article = ArticleFrom(instance=post)
        category_list = models.Category.objects.all()
        category_id = models.Article.objects.filter(id=pk)[0].category_id
        # print('--category_list-->',category_list[0].category_id)
        # print('如果是get的方式,那就先查询')
        return render(request, 'blog/blog_edit.html',
                      {'edit_article': edit_article, 'category_list': category_list, 'category_id': category_id})


def archives(request, y, m):
    """根据年月份列出已发布文章"""
    # posts = models.Article.objects.annotate(num_comment=Count('comment')).filter(
    posts_ar = models.Article.objects.annotate().filter(
            published_date__isnull=False, published_date__year=y,
            published_date__month=m).prefetch_related().order_by('-published_date')
    # for p in posts:
    #     p.click = cache_manager.get_click(p)
    # print('--post_ar-->', posts_ar)
    # for i in posts_ar:
    #     print(i.published_date)
    # print(posts_ar.query)
    return render(request, 'blog/post_list.html',
                  {'posts_ar': posts_ar, 'list_header': '{0}年{1}月'.format(y, m)})


category_obj = models.Category.objects.all()


@login_required
def blog_category(request):
    # global category_obj
    '''
    管理版块列表
    :param request:
    :return:
    '''
    if request.method == "POST":
        edit_id = request.POST.get('id')
        print(edit_id)
        form = CategoryFrom(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.id = edit_id
            post.save()
            return redirect('Earth.views.blog_category')
        else:
            print('数据过大')
    else:
        category_from = CategoryFrom
        category_obj = models.Category.objects.all()
        # print('-->', category_obj)
        # posts = pages(request, blog_all)
        return render(request, 'blog/category_list.html',
                      {'category_obj': category_obj, 'category_from': category_from})


def post_list_by_category(request, cg):
    """根据目录列表已发布文章"""
    posts = models.Article.objects.annotate().filter(
            published_date__isnull=False, category__name=cg).prefetch_related(
            'category').order_by('-published_date')
    # for p in posts:
    #     p.click = cache_manager.get_click(p)
    return render(request, 'blog/post_list.html',
                  {'posts': posts, 'list_header': '\'{}\' 分类的存档'.format(cg)})


@login_required
def blog_category_del(request, pk):
    post = get_object_or_404(models.Category, pk=pk)
    post.delete()
    category_obj = models.Category.objects.all()
    # posts = pages(request, blog_all)
    return render(request, 'blog/table_category.html', {'category_obj': category_obj})

@login_required
def about(request):
    post = get_object_or_404(models.About, pk=1)
    if request.method == "POST":
        form = AboutFrom(request.POST, instance=post)
        print(form)
        if form.is_valid():
            form.save()
            print('ok')
            return HttpResponseRedirect('/blog')
            # return render(request, 'blog/blog_about.html', {'about_obj': form})
    else:
        print('no')
        about_obj = AboutFrom(instance=post)
        # about_obj = models.About.objects.all()
        print(about_obj)
        return render(request, 'blog/blog_about.html', {'about_obj': about_obj, 'is_about': True})


def contact(request):
    contact = models.About.objects.filter(id=2)
    about_obj = models.About.objects.filter(id=1)
    return render(request, 'blog/post_detail.html',
              {'about_obj': about_obj, 'contact': contact})

@login_required
def contact_edit(request):
    post = get_object_or_404(models.About, pk=2)
    if request.method == "POST":
        form = AboutFrom(request.POST, instance=post)
        # print(form)
        if form.is_valid():
            form.save()
            # print('ok')
            return HttpResponseRedirect('/blog')
            # return render(request, 'blog/blog_about.html', {'about_obj': form})
    else:
        # print('no')
        contact_obj = AboutFrom(instance=post)
        # about_obj = models.About.objects.all()
        # print(about_obj.content)
        about_obj = models.About.objects.filter(id=1)

        return render(request, 'blog/blog_about.html', {'contact_obj': contact_obj, 'about_obj': about_obj})
