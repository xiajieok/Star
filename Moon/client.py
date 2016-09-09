# #!/usr/bin/env python2.7
# # coding=utf-8
# import json
# import urllib2
#
# # based url and required header
# url = "http://172.16.0.1:9270/api_jsonrpc.php"
# header = {"Content-Type": "application/json"}
# # request json
# data = json.dumps(
#         {
#             "jsonrpc": "2.0",
#             "method": "host.get",
#             "params": {
#                 "output": ["hostid", "name"],
#                 "filter": {"host": ""}
#             },
#             "auth": "244208ddb1b0f367f0e78d30c241f860",  # the auth id is what auth script returns, remeber it is string
#             "id": 0,
#         })
# # create request object
# # request = urllib2.Request(url, data)
# # for key in header:
# #     request.add_header(key, header[key])
# # # get host list
# # try:
# #     result = urllib2.urlopen(request)
# # except Exception as e:
# #     if hasattr(e, 'reason'):
# #         print 'We failed to reach a server.'
# #         print 'Reason: ', e.reason
# #     elif hasattr(e, 'code'):
# #         print 'The server could not fulfill the request.'
# #         print 'Error code: ', e.code
# # else:
# #     response = json.loads(result.read())
# #     result.close()
# #     print "Number Of Hosts: ", len(response['result'])
# #     for host in response['result']:
# #         print "Host ID:", host['hostid'], "Host Name:", host['name']
# user_data = json.dumps(
#         {
#             "jsonrpc": "2.0",
#             "method": "user.get",
#             "params": {
#                 "output": "extend"
#                 # "output": ["hostid", "name"],
#                 # "filter": {"host": ""}
#             },
#             "auth": "244208ddb1b0f367f0e78d30c241f860",  # the auth id is what auth script returns, remeber it is string
#             "id": 0,
#         })
# request = urllib2.Request(url, user_data)
# for key in header:
#     request.add_header(key, header[key])
# # get host list
# try:
#     result = urllib2.urlopen(request)
# except Exception as e:
#     if hasattr(e, 'reason'):
#         print 'We failed to reach a server.'
#         print 'Reason: ', e.reason
#     elif hasattr(e, 'code'):
#         print 'The server could not fulfill the request.'
#         print 'Error code: ', e.code
# else:
#     response = json.loads(result.read())
#     result.close()
#     print "Number Of Users: ", len(response['result'])
#     user_count = len(response['result'])
#     for user in response['result']:
#         print(user)
#         # print "Host ID:", host['hostid'], "Host Name:", host['name']
#
# # import urllib2
# # import json
# # # based url and required header
# # url = "http://172.16.0.1:9270/api_jsonrpc.php"
# # header = {"Content-Type": "application/json"}
# # # auth user and password
# # data = json.dumps(
# # {
# #     "jsonrpc": "2.0",
# #     "method": "user.login",
# #     "params": {
# #     "user": "Admin",
# #     "password": "41hcH7XAVu2vuP9F"
# # },
# # "id": 0
# # })
# # request = urllib2.Request(url,data)
# # for key in header:
# #     request.add_header(key,header[key])
# # # auth and get authid
# # try:
# #     result = urllib2.urlopen(request)
# # except Exception as e  :
# #     print("Auth Failed, Please Check Your Name And Password:",e)
# # else:
# #     response = json.loads(result.read())
# #     result.close()
# #     print("Auth Successful. The Auth ID Is:",response['result'])
# #
# #
# #
# #
# #
# #
# #
# #
# # req = urllib.request.Request(url = 'http://topic.csdn.net/u/20110123/15/F71C5EBB-7704-480B-9379-17A96E920FEE.html',headers = headers)
# #
# # feeddata = urllib.request.urlopen(req).read()
#
#
# # z = ZabbixAPI(url='http://172.16.0.1:9270', user='Admin', password='41hcH7XAVu2vuP9F')
#
# # Get all monitored hosts
# # result1 = z.host.get(monitored_hosts=1, output='extend')
# # result1 = z.host.get(monitored_hosts=1)
#
# # Get all disabled hosts
# # result2 = z.do_request('host.get',
# #                           {
# #                               'filter': {'status': 1},
# #                               'output': 'extend'
# #                           })
#
# # Filter results
# # hostnames1 = [host['host'] for host in result1]
# # hostnames2 = [host['host'] for host in result2['result']]
# # print(hostnames1)
# # print(hostnames2)
#
#
# # print(z.api_version())
# # or
# # print(z.do_request('apiinfo.version'))
#
# # for i in z.host.get(status=0):
# #     print(i)
# # print(z.do_request('host.getobjects', {'status': 1}))
# # host_list = [host['host'] for host in result1]
# # ip_list = [host['ip'] for host in result1]
# # print(host_list)
# # for i in result1:
# #     print(i)
# #     print(i['status'])
# #     print(i['hostid'])
