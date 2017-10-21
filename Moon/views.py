# from django.http import HttpResponse
from Moon.models import Host
# from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
# from django.contrib.auth.decorators import login_required
# from django.core.urlresolvers import reverse
# from django.shortcuts import redirect
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.db.models import Count
# from django.http import Http404
import json
# import urllib
import sys
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
            groups = group_get_obj['result']
            return groups
        else:
            print('开始查询%s分组' % groupName)
            try:
                group_get_obj = self.__z__.do_request('hostgroup.get',
                                                      {
                                                          'filter': {'name': groupName},
                                                          'output': 'extend'
                                                      })
            except Exception as e:
                print('主机分组不存在 !!!', e)
            else:
                groups = group_get_obj['result']
                print('这里是查询到的group-->', groups)
                for group in groups:
                    self.groupID = group['groupid']
                    return group['groupid']

    def template_get(self, templateName=''):
        if templateName == '':
            template_get_obj = self.__z__.do_request('template.get',
                                                     {
                                                         'output': 'extend'
                                                     })
            templates = template_get_obj['result']
            return templates
        else:
            try:
                print('开始查询%s模板' % templateName)
                response = self.__z__.do_request('template.get',
                                                 {
                                                     'filter': {"name": templateName},
                                                     'output': 'extend'
                                                 })
            except Exception as e:
                print('模板不存在 !!!', e)
            else:
                print('这里是查询模板的结果')
                templates = response['result']
                for template in response['result']:
                    self.templateID = response['result'][0]['templateid']
                return response['result'][0]['templateid']

    def event_get(self):
        try:
            event_get_obj = self.__z__.do_request("event.get", {
                "output": "extend",
            })
        except Exception as e:
            print('事件查询错误 !!!', e)
        else:
            events = event_get_obj['result']
            return events

    def create_host(self):
        pass


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


class Hosts:
    def host_get(self, hostName='', hostStatus='', hostId='', hostip=''):
        '''
        如果status没有值,说明只是查询所有主机记录;
        否则判断ID是否存在,有则输出;
        否则就是在更新主机状态,0为启用,1为禁用.
        :param hostName:
        :param hostStatus:
        :param hostId:
        :return:
        '''
        if hostip:
            print('开始查询全部主机')
            host_get_obj = zabbix().__z__.do_request('host.get',
                                                     {
                                                         'output': 'extend',
                                                     })
            hosts = host_get_obj['result']
            return hosts
        # elif hostip is True:
        else:
            try:
                print('开始查询主机...')
                host_get_obj = zabbix().__z__.do_request('host.get',
                                                         {
                                                             'filter': {'host': hostName},
                                                             'output': 'extend',
                                                         })

            except Exception as e:
                print('主机不存在或者输入主机名错误 !!!', e)
            # else:
            #     hosts = host_get_obj['result']
            #     print('这里是查询到的hosts-->', hosts)
            #     return hosts['hostid']
            else:
                hosts = host_get_obj['result']
                return hosts

    def host_create(self, hostip, hostgroupName, templateName):
        print('这里开始创建,先输出所有的模板信息', templateName)
        if self.host_get(hostip):
            logger.info("该主机已经添加,不要再新建啦!!!!")
            exit(1)
        else:
            group_list = []
            template_list = []
            for i in hostgroupName.split(','):
                # for i in hostgroupName:
                var = {}
                var['groupid'] = zabbix().group_get(i)
                group_list.append(var)
                print('组ID添加好了')

            for i in templateName.split(','):
                '''
                将取到的模板名字使用template_get处理,得到ID;
                将ID添加到template_list,填充数据
                '''
                print('---->', i)
                var = []
                var = zabbix().template_get(i)
                print('var-->', var)

                template_list.append(var)
                for i in template_list:
                    print('这是从列表取出来的模板', i)
                print('模板ID添加好了', template_list)
            try:
                host_create_obj = zabbix().__z__.do_request('host.create', {
                    "host": hostip,
                    "interfaces": [
                        {
                            "type": 1,
                            "main": 1,
                            "useip": 1,
                            "ip": hostip,
                            "dns": "",
                            "port": "10050",
                        }
                    ],
                    "groups": group_list,
                    "templates": template_list

                })
                logger.info('创建主机%s成功...' % hostip)
            except Exception as e:
                logger.warning('新建主机失败 !!!', e)
            else:
                return HttpResponse('ok')

    def host_disabled(self, hostId, hostStatus):
        try:
            print('开始禁用/启用主机 !!!')

            host_get_obj = zabbix().__z__.do_request('host.update',
                                                     {
                                                         "hostid": hostId,
                                                         "status": hostStatus
                                                     })
            hosts = host_get_obj['result']
        except Exception as e:
            print('主机不存在或者输入主机名错误 啊 !!!', e)
        else:
            return hosts

    def host_graphid_get(self, hostname):
        host_graph_get_obj = zabbix().__z__.do_request('host.get', {
            "selectGraphs": ["graphid", "name"],
            "filter": {"host": hostname}
        })
        res = host_graph_get_obj['result']
        # print('数据', res[0]['graphs'])
        # return res[0]['graphs']
        return res

    def host_item_get(self, hostid):
        host_item_get_obj = zabbix().__z__.do_request('item.get', {
            "filter": {"hostids": hostid}
        })
        res = host_item_get_obj['result']
        # print('数据', res[0]['graphs'])
        # return res[0]['graphs']
        print('先获取所有的items', res[0])
        return res

    def graph(self, request):
        try:
            print(request.POST)
            hostname = request.POST.get('hostname')
            print('1 这里是要查询的主机', hostname)
            hosts_graphid = Hosts().host_graphid_get(hostname=hostname)
            print('2 查询出来主机的hostID', hosts_graphid)
            hostid = Hosts().host_get()
            data = hosts_graphid[0]['graphs']
            print('3 这里是根据hostID 查询出来的图形', data)
            for i in data:
                print(i)
            tmp = Hosts().host_item_get(hostid=hostid)
            print('4 这里是tmp,用来取出itemid', tmp)
            # for i in tmp:
            #     print(i)

            items = []
            for value in tmp:
                if '$' in value['name']:
                    name0 = value['key_'].split('[')[1].split(']')[0].replace(',', '')
                    print('name0',name0)
                    name1 = value['name'].split()
                    print('name1',name1)
                    if 'CPU' in name1:
                        name1.pop(-2)
                        name1.insert(1, name0)
                    else:
                        name1.pop()
                        name1.append(name0)
                    name = ''.join(name1)
                    tmpitems = {'itemid': value['itemid'], 'delay': value['delay'], 'units': value['units'],
                                'name': name,
                                'value_type': value['value_type'], 'lastclock': value['lastclock'],
                                'lastvalue': value['lastvalue']}
                else:
                    tmpitems = {'itemid': value['itemid'], 'delay': value['delay'], 'units': value['units'],
                                'name': value['name'], 'value_type': value['value_type'],
                                'lastclock': value['lastclock'],
                                'lastvalue': value['lastvalue']}
                items.append(tmpitems)
                print(items)
                return HttpResponse(json.dumps(data, items))
                # for i in items:
                #     print('这里是添加后的item', i)
        except Exception as e:
            logger.warning('找不到历史数据啊 !!!', e)
        # else:
        #     print('最后的items',items)
        #     print('最后的data',data)
        #

    def history_get(self, itemid, i):
        data = zabbix().__z__.do_request('history.get', {
            "output": "extend",
            "history": i,
            "itemids": itemid,
            "sortfield": "clock",
            "sortorder": "DESC",
            "limit": 10
        })
        res = data['result']
        return res


def up(request):
    logger.info(request.POST)
    try:
        # 获取要更新主机的ID,和新的status
        id = request.POST.get('hostid')
        new_status = request.POST.get('status')
        # host_obj = host().host_get(hostId=id, hostStatus=new_status)
        host_obj = Hosts().host_disabled(hostId=id, hostStatus=new_status)
    except Exception as e:
        logger.warning(e)
    else:
        logger.warning(host_obj)
        return HttpResponse('ok')


def graphs(request):
    data = Hosts.graph(self=None, request=request)
    return HttpResponse(data)


def add(request):
    # hostip, hostgroupName, templateName
    logger.info(request.POST)
    try:
        ip = request.POST.get("hostip")
        group = request.POST.get("hostgroupName")
        print('--> 这里是Add group', group)
        template = request.POST.get("templateName[]")
        print('--> 这里是Add 的template', template)
        host_create = Hosts().host_create(hostip=ip, hostgroupName=group, templateName=template)
    except Exception as e:
        logger.warning(e)
    else:
        return HttpResponse('ok')


def index(request):
    hosts = Hosts().host_get()
    groups = zabbix().group_get()
    users = zabbix().user_get()
    templates = zabbix().template_get()
    events = zabbix().event_get()
    return render(request, 'blog/dash.html',
                  {'hosts': hosts, 'users': users, 'events': events, 'groups': groups, 'templates': templates})


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
