import requests
import os, time
from bs4 import BeautifulSoup
from urllib.request import urlretrieve   #下载数据保存在本地



if __name__ == '__main__':
    # 自动创建文件
    if 'images' not in os.listdir():
        os.makedirs('images')
    list_utl = []
    for num in range(1, 37):
        if num==1:
            url = 'http://www.shuaia.net/meinv/'
        else:
            url = 'http://www.shuaia.net/meinv/index_%d.html'%num
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        html = response.text
        # 遍历文档树
        soup = BeautifulSoup(html, 'lxml')
        # 搜索文档树     find       find_all: 列表
        targe_url = soup.find_all(class_='item-img')
        for each in targe_url:
            list_utl.append(each.img.get('alt') + '->' + each.get('href'))
    print(list_utl)
    print('图片采集完成了!')
    for each_img in list_utl:
        # 分割字符
        img_info = each_img.split('->')
        # 图片的名称
        fileName = img_info[0]+'.jpg'
        # 图片的地址
        targe_img = img_info[1]
        print('下载的数据：' + fileName)
        time.sleep(2)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
        }
        response_img = requests.get(targe_img, headers=headers)
        response_img.encoding = 'utf-8'
        html_img = response_img.text
        # 遍历文档树
        soup_one = BeautifulSoup(html_img, 'lxml')
        # 搜索文档树
        img_url = soup_one.find_all('div', class_='wr-single-content-list')
        # 返回的数据并不是string 而是字节 需要str转换
        soup_two = BeautifulSoup(str(img_url), 'lxml')
        try:
            img_url = soup_two.div.img.get('src')
            urlretrieve(url=img_url, filename='images/' + fileName)
        except :
            img_url = 'http://www.shuaia.net' + soup_two.div.img.get('src')
            urlretrieve(url=img_url, filename='images/' + fileName)