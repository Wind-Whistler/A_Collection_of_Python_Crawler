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
    'User-Agent':'自己填',
    'cookie':'自己填'
    }
for page in range(1,101):
    print(f'正在采集第{page}页数据...')
    #请求网址
    url=f'https://bj.ke.com/ershoufang/pg{page}/' #自己改地址
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