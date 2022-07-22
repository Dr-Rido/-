# coding=utf-8
import parsel
import requests
from lxml.html import etree
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


headers = {
    'cookie': '_S_DPR=1; _S_IPAD=0; tt_webid=7116402967557719566; ttcid=b249285cbe9c44cdb2f4d367bfb8c92251; s_v_web_id=verify_l5c3895w_4iBwwR8l_FGyg_4TJA_8KV8_cpvCIBWFFd6E; local_city_cache=%E9%95%BF%E6%B2%99; csrftoken=b7f9a5659416ee15bc143d60011ca7eb; _S_WIN_WH=1920_937; _tea_utm_cache_24={%22utm_medium%22:%22wap_search%22}; _tea_utm_cache_1300=undefined; MONITOR_WEB_ID=d60c8d6b-f9fd-4b42-87ed-d7f0dd177d84; ttwid=1%7CaXGLP4hVSb3AgEBeaA89sdnboUoIVkitcI14pne1BV4%7C1657267177%7C5c7ff7853f4f2d7920037cab23722f9e236a58ac753f27fc9531e0824195e4b7; tt_scid=VQMNXgztY-Ch3yCZSsvT1xuICMeJP6lqxXR0O48o0Hkf4RN.AMQc7ljkkvFYZJ8Kac88',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}

def get_src(url, file_name):
    # webdriver路径
    service = Service('chromedriver.exe')
    chrome = webdriver.Chrome(service=service)
    chrome.get(url)
    # 强制等待网页加载一下
    sleep(4)
    # chrome.implicitly_wait(5)  # 隐式等待
    # print(chrome.page_source)
    # 点击播放按钮
    is_video = chrome.page_source.find('xg-start-inner')
    if is_video !=-1:
        chrome.find_element(by=By.XPATH, value="//xg-start-inner").click()  # 点击播放
        e = etree.HTML(chrome.page_source)
        # 定位视频播放地址
        src = e.xpath("//video/@src")
        chrome.quit()
        video = requests.get(src[0]).content
        with open(f'{file_name}.mp4', "ab")as f:
            f.write(video)
    else:
        print('该文章没有视频')


def get_text(url):
    response = requests.get(url=url, headers=headers)
    html = response.text
    seleted_data = parsel.Selector(html)
    # print(response.text)
    # 获取标题和文章内容
    titles = seleted_data.xpath("//div[@class='article-content']/h1").getall()
    title = seleted_data.xpath("//div[@class='article-content']/h1/text()").get()
    # print(titles)
    contents = seleted_data.xpath("//article/p/span/text()").getall()
    # print(contents)
    with open(f"{title}.txt", "a",encoding='utf-8')as f:
        f.write(title+'\n')
        if len(contents)>1:
            for i in contents:
                f.write(i+'\n')
        elif len(contents)==0:
            print("content 未获取成功")
        else:
            f.write(contents[0])
    return title


if __name__ == '__main__':
    url = 'https://www.toutiao.com/article/7117537020217442820/'
    title = get_text(url)
    get_src(url, title)
    # 可能因网路原因视频下载会延迟十秒左右
