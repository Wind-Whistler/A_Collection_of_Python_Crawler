#导入数据请求模块
import requests
#导入数据解析模块
import parsel
import re
#导入csv模块
import csv
#创建文件对象
f=open('data.csv','w',encoding='utf-8-sig',newline='')
csv_writer=csv.DictWriter(f,fieldnames=['标题','小区','总价','单价','楼层','层数','年份','户型','面积','朝向'])
csv_writer.writeheader()
#模拟浏览器
headers={
    #User-Agent 用户代理，表示浏览器/设备基本信息
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
    'cookie':'lianjia_uuid=ff9fe31c-9473-4f2d-8ec8-50c708451173; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22196ee1567b89dd-02e9b7188161ba8-4c657b58-1327104-196ee1567b91c46%22%2C%22%24device_id%22%3A%22196ee1567b89dd-02e9b7188161ba8-4c657b58-1327104-196ee1567b91c46%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fcn.bing.com%2F%22%2C%22%24latest_referrer_host%22%3A%22cn.bing.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; select_city=110000; Hm_lvt_b160d5571570fd63c347b9d4ab5ca610=1747751133; HMACCOUNT=DF8307658802DD89; crosSdkDT2019DeviceId=lzt9hs-bohvfg-jt25nfg1bsow4pe-0sdguxh54; login_ucid=2000000081691376; lianjia_token=2.0010d5aa476da8455b017883760176c161; lianjia_token_secure=2.0010d5aa476da8455b017883760176c161; security_ticket=MBj6Om+Wdql1VYw5XD9zzTppOEog77pOFRUtBbMffNsebPn/GqPWyd36hHtX7Fmz0OCyFv6nTicDd5eAIFotB1rdDFdDJUbbUYdWUMcJfj7iqNhAsWGY+d4YsXMWX9LNjRJD4nHaYuNaxxLqb5PNe3unsy7DiUyLgLHs2BF3g7Q=; ftkrc_=a013560b-b365-4480-b2dc-4719b35da05d; lfrc_=35985241-8735-4ce4-aa87-3e9d81a71cd5; lianjia_ssid=b93ade68-540c-4b64-8779-a514a72cfd0f; Hm_lpvt_b160d5571570fd63c347b9d4ab5ca610=1747758546; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiYTk4NDE5YTA1ODhlMjIyZTU4OGZiOTdmM2JlNzQ1NmQ3MjUzM2QyNzRiMTE2MTNhZmFlNGNmNTg3ZDMzMjA4NGJlMzI5ZGQxZWMyZDhjZDVhNTUxOTNlNDA2ODdiOWZkZGRlZmM4MjJmYjY1NDM5ZWIxMTU1NmNmNDY4NjU0YjM3NTViMmQ4ZGM2ZTk0ZGEzYTE3MTg5MGI0NjE0NGY4MDllNWRiNzZlOGIwYTM1ZTQ1NTlmMmYxYTZiMjg4MzU4OTc1MDQzZDE2ZTk1MjQ0MDRjMzg2ZWE4YzcxZTExMzUxODg2ZDhkOGYxNjU5OTI2MDFmM2JlNDZlNTYzNTkxZlwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCIzOTAwNTdlYlwifSIsInIiOiJodHRwczovL2JqLmtlLmNvbS9lcnNob3VmYW5nLyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9'
    }
for page in range(1,101):
    print(f'正在采集第{page}页数据...')
    #请求网址
    url=f'https://bj.ke.com/ershoufang/pg{page}/'
    #发送请求
    response=requests.get(url=url,headers=headers)
    #获取响应数据
    html=response.text
    #把获取的html字符串数据，转成可解析对象
    selector=parsel.Selector(html)
    info_list=re.findall(r'<span class="houseIcon"></span>(.*?)</div>',html,re.S)
    info_list=[i.replace('\n','').replace(' ','') for i in info_list]
    print(info_list)
#     #第一次提取:提取所有房源信息所在标签
#     lis=selector.css('.info')
#     #for循环便利，提取列表里面元素
#     for li,houseInfo in zip(lis,info_list,):
#         #提取每个房源具体数据内容
#         title=li.css('.VIEWDATA::attr(title)').get()  #标题
#         area=li.css('.positionInfo a::text').get()  #小区
#         totalPrice=li.css('.totalPrice span::text').get().strip()  #总价
#         unitPrice=li.css('.unitPrice span::text').get().replace('元/平','')  #单价
#         houseInfo=houseInfo.split('|')
#         houseAera=houseInfo[-2] #面积
#         face=houseInfo[-1] #朝向
#         if len(houseInfo)==3:
#             year='未知'
#             houseType=houseInfo[0].split(')')[-1]    
#             floor=houseInfo[0].split(')')[0] +')'
#         else:
#             floor=houseInfo[0] #楼层
#             year=houseInfo[1] #年代
#             houseType=houseInfo[2] #户型

#         floor_info=floor[:3]
#         floor_num=re.findall('(\d+)',floor)[0]

#         #print(houseInfo)
#         #保存字典
#         dit={
#             '标题':title,
#             '小区':area,
#             '总价':totalPrice,
#             '单价':unitPrice,
#             '楼层':floor_info,
#             '层数':floor_num,
#             '年份':year,
#             '户型':houseType,
#             '面积':houseAera,
#             '朝向':face

#         }
#         csv_writer.writerow(dit)
#         print(dit)

# f.close()