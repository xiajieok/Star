from django.http import HttpResponse
from Moon.models import Host
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import Http404
import json
import urllib
from zabbix.api import ZabbixAPI


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
    return HttpResponseRedirect('/cmdb')


def index(request):
    z = ZabbixAPI(url='http://172.16.0.1:9270', user='Admin', password='41hcH7XAVu2vuP9F')
    # print(z.api_version())
    # return HttpResponse(z.api_version())
    host_obj = z.do_request('host.get',
                             {
                                 # 'filter': {'status': 0},
                                 'output': 'extend',
                             })
    # hostnames = [host['host'] for host in host_obj['result']]
    hosts =  host_obj['result']

    # print(type(host_obj['result']))

    for i in host_obj['result']:
        print(i)

    host_count = len(host_obj['result'])
    print(host_count)
    # hostnames = [host['hostid'] for host in host_list['result']]
    # for i in host_list['result']:
        # print(i['host'])
    # print(hostnames)

    user_count = z.do_request('user.get',
                              {
                                  "output": "extend",
                              }
                              )
    user_count = len(user_count)

    return render(request, 'blog/dash.html', {'hosts': hosts,'user_count':user_count,'host_count':host_count})


def info(req):
    print(req)
    if req.method == 'POST':
        hostname = req.POST.get('hostname')
        ip = req.POST.get('ip')
        OS = req.POST.get('os')
        memory = req.POST.get('memory')
        disk = req.POST.get('disk')
        vendor_id = req.POST.get('vendor_id')
        # model_name = req.POST.get('model_name')
        cpu_core = req.POST.get('cpu')
        product = req.POST.get('product')
        Manufacturer = req.POST.get('Manufacturer')
        sn = req.POST.get('sn')
        try:
            host = Host.objects.get(hostname=hostname)
        except:
            host = Host()

        host.hostname = hostname
        host.ip = ip
        host.os = OS
        host.memory = memory
        host.disk = disk
        host.vendor_id = vendor_id
        # host.model_name = model_name
        host.cpu_core = cpu_core
        host.product = product
        host.Manufacturer = Manufacturer
        host.sn = sn
        host.save()

        return HttpResponse('ok')
    else:
        return HttpResponse('no data')
