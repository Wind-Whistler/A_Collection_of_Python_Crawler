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
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
    'cookie':'aQQ_ajkguid=0D420177-A034-8F1A-DC9A-7A93C6D5191D; ctid=11; ajk-appVersion=; fzq_h=4bbca8eed746da45e5bb6ceb8e7beacd_1747815344893_0762fd4bb28f40efb71b5124f8e5b952_2026648997; id58=CrIHZ2gti7JiFP+1BhFkAg==; xxzlclientid=fc625cd4-fbfa-4198-b5fc-1747815350061; xxzlxxid=pfmxen1cLwUO60m1zfVwXAzt1CFyLQwcWPA6uRw/N3Cx+kIg/Oeb32aHbX1BsiVioGrU; twe=2; sessid=8503B866-4351-828A-FB60-8933607AB9BE; ajk_member_verify=paqpfLKCWGD%2BZHEUTrmWBHMT%2BTN33S26BY53aBEhNO4%3D; ajk_member_verify2=MzA5Nzg0NjAyfHBqZmRrVUV8MQ%3D%3D; fzq_js_anjuke_ershoufang_pc=a1d5492604af2512c6798890460c94c5_1747898557642_25; obtain_by=1; ajkAuthTicket=TT=be5779e2a0c710da0ea30145bb936be8&TS=1747898553813&PBODY=FNAVIEWXm11I9-Si6w89Y7i6ycBSWNW47RqzImJpnTbllToH53Ea64tfdAhTUkYEWrxo-JlTiLQjL8s0lyNa7v3Se-mekOnyWQIfZHlB3Ho84Tp0WuRFMWSC8Mdc9SQvPtZTiJafcWXa17FY7kvUnKBL-tImes0IAnZ76DMATH0&VER=2&CUID=nenOnjazC6X_U7AiOtHvjHKyO1Hvr8W-; xxzlbbid=pfmbM3wxMDM0NnwxLjEwLjB8MTc0Nzg5ODU1ODYxMjc2NzQwNnxENm1BRWduSmZuZHRvUlY3ZkNCREYyTmVabk1Wd3ZDNmpoVlprQ1NkT2hnPXxjMjg3MmQwNTQwY2JkZjRiMjRlY2EwNmU2YjAyYWE5NV8xNzQ3ODk4NTUzNTk3X2VhNTcwYjVlZmY3ODQ5NTdiYjA0ZTcyNWI5NDc1MGI0XzMwODI4Nzg4MTF8Nzc4Y2UxMDg4NGQyMGEwZDNlZDU3NzJmYzVlNjIzNTlfMTc0Nzg5ODU1ODE1M18yNTY='
    }
for page in range(1,300):
  print(f'正在采集第{page}页数据...')
  #请求网址
  url=f'https://shanghai.anjuke.com/sale/p{page}/?from=HomePage_TopBar'
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
  


  
    
    
  
