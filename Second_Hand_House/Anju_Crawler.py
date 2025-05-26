#导入数据请求模块
import requests
#导入数据解析模块
import parsel
import re
#导入csv模块
import csv
#创建文件对象
f=open('Beijing_data.csv','w',encoding='utf-8-sig',newline='')
csv_writer=csv.DictWriter(f,fieldnames=['标题','年代','地址','户型','面积','朝向','楼层','总价','单价'])
csv_writer.writeheader()
#模拟浏览器
headers={
    #User-Agent 用户代理，表示浏览器/设备基本信息
    'User-Agent':'按照你的浏览器来填',
    'cookie':'按照你的浏览器来填'
    }
for page in range(1,300):
  print(f'正在采集第{page}页数据...')
  #请求网址
  url=f'https://shanghai.anjuke.com/sale/p{page}/?from=HomePage_TopBar' #可以自己换别的地区
        #发送请求
  response=requests.get(url=url,headers=headers)
        #获取响应数据
  html=response.text
        #把获取的html字符串数据，转成可解析对
  selector=parsel.Selector(html)

    #     #第一次提取:提取所有房源信息所在标签
  lis = selector.css('.property')

    #     for循环便利，提取列表里面元素
  for div in lis:
    #     提取每个房源具体数据内容
    title=div.css('.property-content-title h3::attr(title)').get()  #标题
    info_text = div.css('.property-content-info-text')
    spans = info_text.css('span::text').getall()
    house_type = ''.join(spans) #户型
    info_texts = div.css('.property-content-info-text')
    area = None #面积
    for info_text in info_texts:
        text = info_text.get()
        if '㎡' in text:
            area = text.strip().replace('</p>', '').replace(' ','').replace('<pclass="property-content-info-text"data-v-2c97aebe>','') .replace('\n','')# 保留单位，去除前后空白字符
            break
    orientation = None #朝向
    for info_text in info_texts:
        text = info_text.get()
        if '东' in text or '西' in text or '南' in text or '北' in text:
            orientation = text.strip().replace('</p>', '').replace(' ','').replace('<pclass="property-content-info-text"data-v-2c97aebe>','') .replace('\n','') 
            break
    floor=None #楼层
    for info_text in info_texts:
        text = info_text.xpath('normalize-space()').get()
        if text is None:
            continue
        if '层' in text:
            floor = text.strip()
            break
        else:
            floor = '未知'
    year=None #年份
    for info_text in info_texts:
        text = info_text.xpath('normalize-space()').get()
        if text is None:
            continue
        if '建造' in text:
            year = text.strip().replace('年建造','')
            break
        else:
            year = '未知'
    comm_name_element = div.css('.property-content-info-comm-address')
    comm_name = comm_name_element.css('span::text').get() #地区
    total_price_element = div.css('.property-price-total-num')
    total_price = total_price_element.css('::text').get() #总价
    unit_price_element = div.css('.property-price-average')
    unit_price = unit_price_element.css('::text').get().replace('元/㎡','').replace(' ','').replace('\n','')#单价
    print(unit_price)
    dit={
            '标题': title,
            '年代':  year,    
            '地址': comm_name,
            '户型' : house_type,
            '面积' : area,
            '朝向' : orientation,
            '楼层' : floor,
            '总价': total_price,
            '单价': unit_price
        }
    csv_writer.writerow(dit)
    print(dit)

f.close()  
  


  
    
    
  
