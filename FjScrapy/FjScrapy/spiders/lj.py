import scrapy


class LjSpider(scrapy.Spider):
    name = 'lj'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://bj.lianjia.com/ershoufang/pg1/']
    page = 1

    '''翻页'''
    # 优先获取url列表:  （广度优先）
    # def start_requests(self):
    #     for i in  range(1,11):
    #         yield scrapy.Request(f'https://bj.lianjia.com/ershoufang/pg{i}/')

    def parse(self, response, **kwargs):
        url_list = response.xpath("//div[@class='info clear']/div/a/@href").getall()
        for url in url_list:
            yield scrapy.Request(url, callback=self.parse_info)

        '''翻页：优先获取房源信息  （深度优先）'''
        if self.page <= 11:
            self.page += 1
            yield scrapy.Request(f'https://bj.lianjia.com/ershoufang/pg{self.page}/')

    def parse_info(self,response):
        title = response.xpath("//div[@class='title']/h1/text()").get()
        price = response.xpath("//span[@class='total']/text()").get()
        community = response.xpath("//div[@class='communityName']/a[1]/text()").get()
        area = response.xpath("string(//div[@class='areaName']/span[2])").get()
        base = response.xpath("//div[@class='base']/div[@class='content']")
        house_type = base.xpath("./ul/li[1]/text()").get()
        house_floor = base.xpath("./ul/li[2]/text()").get()
        house_area = base.xpath("./ul/li[3]/text()").get()
        house_lift = base.xpath("./ul/li[last()]/text()").get()
        house_warmmer = base.xpath("./ul/li[last()-1]/text()").get()

        yield {
            "title": title,
            "price": price,
            "community": community,
            "area": area,
            "house_type": house_type,
            "house_floor": house_floor,
            "house_area": house_area,
            "house_lift": house_lift,
            "house_warmmer": house_warmmer,
        }
