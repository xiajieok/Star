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
import json
import markdown
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache


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
            return HttpResponseRedirect(request.GET.get('next') or '/')
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


def index(request):
    #     return HttpResponse('hello')
    # # def index(request):
    # # # def post_list(request):
    '''所有已发布文章'''
    blog_all = models.Article.objects.annotate(num_comment=Count('id')).filter(published_date__isnull=False).order_by(
            '-published_date').exclude(title='About')
    # blog_all = models.Article.objects.all()
    posts = pages(request, blog_all)
    # about_obj = models.About.objects.values().all()
    # tag_obj = models.Tag.objects.values().all()
    category_obj = models.Category.objects.values().all().exclude(name='About')
    return render(request, 'index.html',
                  {'posts': posts, 'page': True,
                   })


def side(request):
    res = request.GET.get('name')
    key = res

    print(request)
    if res == 'tag':
        obj = models.Tag.objects.values().all()
    elif res == 'category':
        obj = models.Category.objects.values().all()
    elif res == 'about':
        obj = models.About.objects.values()
    else:
        '''
        获取ID,根据ID+1,-1来获取上一篇和下一篇；
        '''
        ids = request.GET.get('id')
        obj1 = models.Article.objects.values('id', 'title').filter(id__gt=ids)[0:1]
        ltID = int(ids) - 1
        tmp_obj2 = models.Article.objects.values('id', 'title').filter(id=ltID)
        while len(tmp_obj2) == 0:
            ltID = ltID - 1
            tmp_obj2 = models.Article.objects.values('id', 'title').filter(id=ltID)

        obj2 = tmp_obj2
        li = []
        for i in list(obj1):
            obj = {'id': i['id'], 'title': i['title']}
            li.append(obj)
        for i in list(obj2):
            obj = {'id': i['id'], 'title': i['title']}
            li.append(obj)
        obj = li

    data = list(obj)
    data = json.dumps(data)
    return HttpResponse(data)


def post_detail(request, pk, refresh=False):
    post = get_object_or_404(models.Article, pk=pk)

    key = 'title-%s' % (pk)
    print(key)
    value = cache.get(key)
    print(value)
    if value and not refresh:
        views_obj = models.Article.objects.filter(id=pk).values('views')
        obj = list(views_obj)
        for i in obj:
            tmp = i['views'] + 1
            models.Article.objects.filter(id=pk).update(views=tmp)
        return render(request, 'front/post_detail.html',
                      {'post': post,'content': post.content, 'is_post': True})
    else:
        # body = markdown.markdown(post.md, )
        # md = post.md
        print(post.content)
        cache.set(key, post.content, 2 * 24 * 3600)
        pass

    views_obj = models.Article.objects.filter(id=pk).values('views')
    obj = list(views_obj)
    for i in obj:
        tmp = i['views'] + 1
        models.Article.objects.filter(id=pk).update(views=tmp)
    return render(request, 'front/post_detail.html',
                      {'post': post,'content': post.content, 'is_post': True})


@login_required
def blog_new(request):
    print(request.method)
    if request.method == "POST":
        try:
            # 判断用户名是否被注册
            models.Article.objects.get(title=request.POST.get('title'))
        except ObjectDoesNotExist:
            form = ArticleFrom(request.POST)
            print('这里是post的request', request.POST)
            print('这里是post的form', form)
            # if form.is_valid():
            form_data = form.cleaned_data
            form_data['author_id'] = request.user.userprofile.id
            print('ID--->', request.POST.get('category_id'))
            form_data['category_id'] = request.POST.get('category_id')
            form_data['tags_id'] = request.POST.get('tags_id')
            form_data['content'] = request.POST.get('text')
            form_data['md'] = request.POST.get('editormd-markdown-doc')
            print('--->form_data', form_data)

            new_article_obj = models.Article(**form_data)
            new_article_obj.save()

            # post = form.save(commit=False)
            print(new_article_obj)
            return redirect('/drafts/')
            # else:
            #     print('NO !!!!!!!!!!!!!!!')
        # raise forms.ValidationError('文章标题冲突')
        category_list = models.Category.objects.all()
        tags_list = models.Tag.objects.all()
        return render(request, 'admin/blog_edit.html',
                      {'category_list': category_list, 'tags_list': tags_list, 'is_new': True})

    else:
        # form = models.Post.objects.all()
        new_article = ArticleFrom()
        category_list = models.Category.objects.all()
        tags_list = models.Tag.objects.all()
        # print('这里是get的form',form)
    return render(request, 'admin/blog_edit.html',
                  {'new_article': new_article, 'category_list': category_list, 'tags_list': tags_list, 'is_new': True})


@login_required
def blog_publish(request, pk):
    print(pk)
    post = get_object_or_404(models.Article, pk=pk)
    post.publish()
    # return redirect('Earth.views.post_detail', pk=pk)
    blog_all = models.Article.objects.filter(published_date__isnull=True).order_by('-created_date')
    posts = pages(request, blog_all)
    return render(request, 'admin/table.html', {'posts': posts})


@login_required
def blog_remove(request, pk):
    post = get_object_or_404(models.Article, pk=pk)
    post.delete()
    blog_all = models.Article.objects.annotate(num_comment=Count('id')).filter(published_date__isnull=False).order_by(
            '-published_date')
    posts = pages(request, blog_all)
    return render(request, 'admin/table.html', {'posts': posts})


def edit(request):
    print(request.POST)
    res = request.POST.get('type')
    name = request.POST.get('name')
    if res == 'cg':
        alias = request.POST.get('alias')
        models.Category.objects.create(name=name, alias=alias)
    else:
        models.Tag.objects.create(name=request.POST.get('name'))

    return HttpResponse(True)


@login_required
def blog_admin(request):
    return render(request, 'admin/blog_list.html')


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
    return render(request, 'admin/blog_list.html', {'posts': posts, 'page': True, 'is_list': True})


@login_required
def blog_drafts(request):
    '''
    管理后台草稿箱列表
    :param request:
    :return:
    '''
    blog_all = models.Article.objects.filter(published_date__isnull=True).order_by('-created_date')
    posts = pages(request, blog_all)
    return render(request, 'admin/blog_list.html', {'posts': posts, 'page': True})


@login_required
def blog_edit(request, pk):
    print(request.method, request.POST)
    post = get_object_or_404(models.Article, pk=pk)
    print(post)
    # print(request.method,"-------->")
    if request.method == "POST":

        content = request.POST.get('text')
        md = request.POST.get('editormd-markdown-doc')
        print(pk, md)
        s = models.Article.objects.filter(id=pk).values('md')
        print('sss', s)
        obj = models.Article.objects.filter(id=pk).update(md=md, content=content)
        print(obj)
        '''
        保存成功后跳转到详情页
        '''
        return redirect(reverse('detail', args=[pk]))
    else:
        edit_article = ArticleFrom(instance=post)
        category_list = models.Category.objects.all()
        category_id = models.Article.objects.filter(id=pk)[0].category_id
        # print('--category_list-->',category_list[0].category_id)
        # print('如果是get的方式,那就先查询')
        ss = edit_article
        print('sssssssssssss', ss)

        ar = models.Article.objects.filter(id=pk).values('md')
        print('ar', ar)

        return render(request, 'admin/blog_edit.html',
                      {'edit_article': ar})


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
    return render(request, 'front/post_list.html',
                  {'posts_ar': posts_ar, 'list_header': '{0}年{1}月'.format(y, m)})


category_obj = models.Category.objects.all()


@login_required
def admin_category(request):
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
        return render(request, 'admin/category_list.html',
                      {'category_obj': category_obj, 'category_from': category_from})


def post_list_by_category(request, cg):
    """根据目录列表已发布文章"""
    posts = models.Article.objects.annotate().filter(
            published_date__isnull=False, category__name=cg).prefetch_related(
            'category').order_by('-published_date')
    # for p in posts:
    #     p.click = cache_manager.get_click(p)
    return render(request, 'index.html',
                  {'posts': posts, 'list_header': '\'{}\' 分类的存档'.format(cg)})


@login_required
def blog_category_del(request, pk):
    post = get_object_or_404(models.Category, pk=pk)
    post.delete()
    category_obj = models.Category.objects.all()
    # posts = pages(request, blog_all)
    return render(request, 'admin/table_category.html', {'category_obj': category_obj})


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
        return render(request, 'admin/blog_about.html', {'about_obj': about_obj, 'is_about': True})


def contact(request):
    contact = models.About.objects.filter(id=2)
    about_obj = models.About.objects.filter(id=1)
    return render(request, 'front/post_detail.html',
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

        return render(request, 'admin/blog_about.html', {'contact_obj': contact_obj, 'about_obj': about_obj})


def category(request, arg):
    arg = arg
    print(arg)
    blog_all = models.Article.objects.filter(category__name=arg).order_by(
            '-published_date')
    print(blog_all)
    posts = pages(request, blog_all)
    about_obj = models.About.objects.values().all()
    tag_obj = models.Tag.objects.values().all()
    category_obj = models.Category.objects.values().all()
    return render(request, 'index.html',
                  {'posts': posts, 'is_post': True, 'about_obj': about_obj, 'category_obj': category_obj,
                   'tag_obj': tag_obj})


def tags(request, tag):
    tag = tag
    blog_all = models.Article.objects.filter(tags__name=tag).order_by(
            '-published_date')
    print(blog_all)
    posts = pages(request, blog_all)
    about_obj = models.About.objects.values().all()
    tag_obj = models.Tag.objects.values().all()
    category_obj = models.Category.objects.values().all()
    return render(request, 'index.html',
                  {'posts': posts, 'is_post': True, 'about_obj': about_obj, 'category_obj': category_obj,
                   'tag_obj': tag_obj})


def robot(request):
    data = {'title': request.POST.get('title'),
            'brief': request.POST.get('brief'),
            'content': request.POST.get('article'),
            'reprinted': request.POST.get('reprinted'),
            'published_date': request.POST.get('date'),
            'author_id': '1', 'category_id': '1', 'tags_id': '5'
            }
    # print(request.POST)
    models.Article.objects.update_or_create(**data)
    # print('这里是post的request', request.POST)
    # title = res.title
    # print(title)
    # models.Article.objects.create(**res)


    return HttpResponse('ok')
