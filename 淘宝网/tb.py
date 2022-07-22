import json
import parsel
import requests
import re
from time import sleep

def send_req(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49',
        'Cookie': 'cna=tujlFseX6VQCARsXV2aFIXcj; miid=1842972687209524589; tracknick=tb654604602; enc=/lYri0sIgIUOTHYTzZy1iNJrica8Zi3x7NxRh3lBcBscsJ/MHn4BpckL4Cy/Tezxkjunm3eo5WVXex5rYpJQaLWAPWIY9q+i2jEFT4JX6y4=; t=3b895a91ebbc3a646c2be5ada1595484; sgcookie=E100mVzt32I8FaWjDxfXQNex1L5yZtQF7WRGJlfCbAVfKzjzR2B6gjQeueHz2kVyvOoOsqxbc00o7I59ze3ZxVOXGEqgKFQVSCNPvndDYaTlp8TcvW/j7pPo+k8UePojCL3T; uc3=vt3=F8dCvCPaKDH64w7zqks=&lg2=VT5L2FSpMGV7TQ==&id2=UUphyu7jVL7RLUVmVA==&nk2=F5RDKXH8EDNut1I=; lgc=tb654604602; uc4=nk4=0@FY4I6gVc46/MneS9LJUg2H7hzMbkyQ==&id4=0@U2grEagn5RiVCTiB4bLpG28vsJKLt6Lh; _cc_=V32FPkk/hw==; thw=cn; _m_h5_tk=e56268a2c5395feda8826ee23862d508_1657505908682; _m_h5_tk_enc=a58b7d1efb88aecc9e4621679cb0628c; xlly_s=1; cookie2=1763ced6607ecbaf1385a3db70824a51; _tb_token_=ee181f3ee5d35; mt=ci=-1_0; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; uc1=cookie14=UoexNTXrOoCUow==; JSESSIONID=AD33E4BBE9E9C1F3F1D765E21A0232FE; isg=BBwcuRevkuSYXGY6yIdYA8xO7TrOlcC_A4nlBPYdDIfqQb3LHqSYTgK4pam5TfgX; l=eBTZmi9gLfcBZ4jOBOfanurza77OSIRYmuPzaNbMiOCP_z1B5hPCW6AGcFL6C3GVh6veR3ud9SS9BeYBq6CKnxvtIosM_Ckmn; tfstk=c6jRBpq3ESVkYIzcl6UDY7UaGDNGa0kJtYOKvMNaMRLQxAijDsvhjGhOKz9e_QeA.'
    }
    resp = requests.get(url=url, headers=headers)
    html = resp.text
    return html


def save_data(tb_html):
    selected_data = parsel.Selector(tb_html)
    # print(html)
    g_page_config = selected_data.xpath('//script')
    json_data = re.findall('g_page_config = (.*?),"recommendAuctions":', tb_html)[0]+'}}}}'
    # print(json_data)
    json_dict = json.loads(json_data, strict=False)  # 字符串中允许使用控制字符(换行符、制表符)

    # print(json_dict)
    infos = json_dict['mods']['itemlist']['data']['auctions']
    # print(info)
    with open('商品信息.csv', 'a', encoding='utf-8')as f:
        for info in infos:
            title = info['title'].replace(' ', '')
            raw_title = info['raw_title'].replace(' ', '')
            item_loc = info['pic_url'].replace(' ', '')
            detail_url = info['detail_url'].replace(' ', '')
            view_price = info['view_price'].replace(' ', '')
            view_sales = info['view_sales'].replace(' ', '')
            pic_url = info['pic_url'].replace(' ', '')
            user_id = info['user_id'].replace(' ', '')
            nick = info['nick'].replace(' ', '')
            # print(title)
            content = f'{title}|{raw_title}|{item_loc}|{detail_url}|{view_sales}|{view_sales}|{pic_url}|{user_id}\n'
            f.write(content)


if __name__ == '__main__':
    for i in range(6):
        url = f'https://s.taobao.com/search?spm=a21bo.jianhua.201867-main.13.f98c11d9Vp1PDn&q=%E6%89%8B%E6%9C%BA&s={i*44}'
        html_data = send_req(url)
        save_data(html_data)
        sleep(3)

