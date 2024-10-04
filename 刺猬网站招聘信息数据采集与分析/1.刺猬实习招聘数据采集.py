# 本次项目使用的数据需要自行使用爬虫工具进行采集，主要采集的数据包含岗位名称,公司名称,薪资待遇,学历要求,实习时长,工作描述,发布时间,招聘人数,工作地点,企业领域等。
# 主要采集的网页为：https://www.ciwei.net
import pandas
import requests
from lxml import etree
import pandas as pd
import csv

def request1(url):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
    res=requests.get(url,headers=headers)
    return res

"""一级界面内容解析"""
def parse_data(res):
    # 数据解析
    html=etree.HTML(res.text)

    # 1.岗位名称
    job_name=html.xpath('//div[@class="job-item___18L91"]/div/div/div/div/a/span/i/text()')
    # 2.薪资待遇
    salary=html.xpath('//div[@class="job-item___18L91"]/div/div/div/div[2]/span[1]/text()')
    # 3.实习时长
    internship_time=html.xpath('//div[@class="job-item___18L91"]/div/div/div/div[2]/span/span[3]/text()')
    # 4.岗位详情网址
    job_details_url=html.xpath('//div[@class="job-item___18L91"]/div/div/div/div/a/@href')
    job_details_url_list=[]
    for i in job_details_url:
        url1='https://www.ciwei.net'+i
        job_details_url_list.append(url1)

    # 5.公司详情网址
    company_details_url=html.xpath('//div[@class="job-item___18L91"]/div/div[3]/a/@href')
    company_details_url_list=[]
    for i in company_details_url:
        url2='https://www.ciwei.net/'+i;
        company_details_url_list.append(url2)

    data=zip(job_name,salary,internship_time,job_details_url_list,company_details_url_list)
    return data
    # print(pd.DataFrame({'job_name':job_name,'salary':salary,'internship_time':internship_time,'job_details_url':job_details_url_list,'company_details_url':company_details_url_list}))

"""二级界面内容解析"""
def parse_data1(data):

    job_name=data[0]#公司名称
    salary=data[1]#薪资
    internship_time=data[2]#实习时长
    job_url=data[3]
    res=request1(job_url)
    html = etree.HTML(res.text)

    # 1.工作描述
    job_descript=''.join(html.xpath('//ul[@class="job-desc___3DHRK"]//text()'))

    # 2.学历要求
    education_requirement=html.xpath('//*[@id="root"]/div/div/section/main/section/div/div[1]/div/div[1]/p[1]/span[2]/text()')[1]
    # 3.招聘人数
    recruit_people=html.xpath('//*[@id="root"]/div/div/section/main/section/div/div[1]/div/div[1]/p[1]/span[2]/text()')[2]+'人'
    # 4.发布时间
    release=html.xpath('//*[@id="root"]/div/div/section/main/section/div/div[1]/div/div[1]/p[2]/text()')[0]
    # 5.公司名称
    company_name=html.xpath('//*[@id="root"]/div/div/section/main/section/div/div[3]/div[2]/div[2]/a/span[1]/text()')[0]
    # 6.公司地址
    company_address=''.join(html.xpath('//p[@class="address-detail___20TdD"]//text()'))
    # 7.企业领域
    try:
        enterprise_sector=html.xpath('//div[@class="right-wrap___Cn5vb"]/div[2]/ul/li[2]/span[2]/text()')[0]
    except:
        return
    # 8.公司规模
    company_size=html.xpath('//div[@class="right-wrap___Cn5vb"]/div[2]/ul/li[1]/span[2]/text()')[0]

    data_all=(job_name,salary,internship_time,job_descript,education_requirement,recruit_people,release,company_name,company_address,enterprise_sector,company_size)
    return data_all
    # print(job_descript)
    # print(education_requirement)
    # print(recruit_people)
    # print(release)
    # print(company_name)
    # print(company_address)
    # print(enterprise_sector)
    # print(company_size)


# "工作岗位","薪资待遇","实习时长","工作描述","学历要求","招聘人数","发布时间","公司名称","公司地址","企业领域"和"公司规模"。
"""csv库进行存储数据"""
def save1(data,flag):
    with open('./data.csv','a+',encoding='GB18030',newline='')as cs_file:
        writer=csv.writer(cs_file)
        if flag:
            writer.writerow(["工作岗位","薪资待遇","实习时长","工作描述","学历要求","招聘人数","发布时间","公司名称","公司地址","企业领域","公司规模"])
        writer.writerow([data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10]])
    print('数据保存成功！！！')



if __name__=='__main__':
    flag=False
    a=0


    url_list=['https://www.ciwei.net/internship/search/sc1']
    for i in range(2,50):
        url = f'https://www.ciwei.net/internship/search/sc1-pg{i}'
        url_list.append(url)


    for j in url_list[15:]:
        print(f'正在爬取:{j}')
        res=request1(j)
        data0=parse_data(res)

        for data in data0:
            data1=parse_data1(data)
            if data1:
                if a > 0:
                    flag = False
                save1(data1,flag)
                a += 1





