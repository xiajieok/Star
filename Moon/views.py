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
import logging

# 用字典保存日志级别
format_dict = {
    1: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
    2: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
    3: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
    4: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
    5: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
}


class zabbix:
    def __init__(self):
        try:
            self.__z__ = ZabbixAPI(url='http://192.168.40.11/zabbix', user='admin', password='zabbix')
            # self.__z__ = ZabbixAPI(url='http://172.16.0.1:9270', user='Admin', password='41hcH7XAVu2vuP9F')

        except Exception as e:
            print('用户认证失败,请检查 !!!', e)

    def host_get(self, hostName='', hostStatus='', hostId=''):
        '''
        如果status没有值,说明只是查询所有主机记录;
        否则判断ID是否存在,有则输出;
        否则就是在更新主机状态,0为启用,1为禁用.
        :param hostName:
        :param hostStatus:
        :param hostId:
        :return:
        '''
        if hostStatus == '':
            host_get_obj = self.__z__.do_request('host.get',
                                                 {
                                                     'output': 'extend',
                                                 })
            hosts = host_get_obj['result']
            return hosts
        elif hostId is True:
            try:
                print('开始查询主机...')
                host_get_obj = self.__z__.do_request('host.get',
                                                     {
                                                         'filter': {'host': hostName},
                                                         'output': 'extend',
                                                     })
                hosts = host_get_obj['result']
                return hosts
            except Exception as e:
                print('主机不存在或者输入主机名错误 !!!', e)
        else:
            try:
                print('开始禁用/启用主机 !!!')

                host_get_obj = self.__z__.do_request('host.update',
                                                     {
                                                         "hostid": hostId,
                                                         "status": hostStatus
                                                     }
                                                     )
                hosts = host_get_obj['result']
                return hosts
            except Exception as e:
                print('主机不存在或者输入主机名错误 啊 !!!', e)

    def user_get(self, userName=''):
        if userName == '':
            user_get_obj = self.__z__.do_request('user.get',
                                                 {
                                                     'output': 'extend',
                                                 })
        else:
            try:
                user_get_obj = self.__z__.do_request('user.get',
                                                     {
                                                         'filter': {'name': userName},
                                                         'output': 'extend',
                                                     })
            except Exception as e:
                print('主机不存在或者输入主机名错误 !!!', e)

        users = user_get_obj['result']
        return users

    def group_get(self, groupName=''):
        if groupName == '':
            group_get_obj = self.__z__.do_request('hostgroup.get',
                                                  {
                                                      'output': 'extend'
                                                  })
        else:
            try:
                group_get_obj = self.__z__.do_request('hostgroup.get',
                                                      {
                                                          'filter': {'name': groupName},
                                                          'output': 'extend'
                                                      })
            except Exception as e:
                print('主机分组不存在 !!!', e)
        groups = group_get_obj['result']
        return groups

    def template_get(self, templateName=''):
        if templateName == '':
            template_get_obj = self.__z__.do_request('template.get',
                                                     {
                                                         'output': 'extend'
                                                     })
        else:
            try:
                template_get_obj = self.__z__.do_request('template.get',
                                                         {
                                                             'filter': {"name": templateName},
                                                             'output': 'extend'
                                                         })
            except Exception as e:
                print('模板不存在 !!!', e)
        templates = template_get_obj['result']
        return templates

    def event_get(self):
        try:
            event_get_obj = self.__z__.do_request("event.get", {
                "output": "extend",
                # "select_acknowledges": "extend",
                # "sortfield": ["clock", "eventid"],
                # "sortorder": "DESC"
            })
        except Exception as e:
            print('事件查询错误 !!!', e)
        else:
            events = event_get_obj['result']
            return events


class Logger():
    def __init__(self, logname, loglevel, logger):
        """
            指定保存日志的文件路径,日志级别,以及调用文件;
            将日志存入到指定文件中
        """
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler,用于写入日志文件
        fh = logging.FileHandler(logname)
        fh.setLevel(logging.DEBUG)

        # 再创建一个handle,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = format_dict[int(loglevel)]
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger


logger = Logger(logname='cmdb_log.txt', loglevel=1, logger="cmdb").getlog()

z = ZabbixAPI(url='http://192.168.40.11/zabbix', user='admin', password='zabbix')


def up(request):
    # print('----post---->', request.POST)
    id = request.POST.get('hostid')
    # print('hostid', id)
    new_status = request.POST.get('status')
    # print('status', new_status)
    logger.info(request.POST)
    try:
        host_obj = zabbix().host_get(hostId=id, hostStatus=new_status)
    except Exception as e:
        logger.warning(e)
        return HttpResponse('no')
    else:
        logger.warning(host_obj)
        return HttpResponse('ok')


def index(request):
    hosts = zabbix().host_get()
    groups = zabbix().group_get()
    users = zabbix().user_get()
    events = zabbix().event_get()
    return render(request, 'blog/dash.html',
                  {'hosts': hosts, 'users': users, 'events': events, 'groups': groups})


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
