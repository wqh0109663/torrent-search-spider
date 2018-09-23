# -*- coding: utf-8 -*-
import scrapy
import base64
import time


class TorrentsearchSpider(scrapy.Spider):
    name = 'torrentsearch'
    allowed_domains = ['onionsearch.net']
    start_urls = ['http://www.onionsearch.net/search/' + input("please input resource name : ")]

    def parse(self, response):
        size_list = response.xpath("//div[@class='search-item']//span[@class='list-value'][2]/text()").extract()
        for i in range(len(size_list)):

            if "GB" in size_list[i]:
                size_list[i] = float(size_list[i].strip().split("G")[0].strip()) * 1024
            elif "MB" in size_list[i]:
                size_list[i] = float(size_list[i].strip().split("M")[0].strip())
            else:
                size_list[i] = 0
        copy_list = size_list
        size_list = sorted(size_list, key=float)
        sublist = size_list[-5:]
        list_url = []
        select = 0
        for i in range(len(sublist)):
            index = copy_list.index(sublist[i])
            title = "".join(response.xpath("(//span[@class='list-title'])[{0}]//text()".format(index)).extract())
            size = response.xpath("(//span[@class='list-value'][2])[{0}]/text()".format(index)).extract_first()
            file_num = response.xpath("(//span[@class='list-value'][3])[{0}]/text()".format(index)).extract_first()
            link_url = response.xpath("(//span[@class='list-label'][4])[{0}]/a/@href".format(index)).extract_first()
            list_url.append(link_url)
            select = select + 1
            print("{0}. 内容: {1} , 文件大小: {2} , 文件数:{3}".format(select, title, size, file_num))
        while (1):
            input_str = input("请选择下载那个： ")
            print()
            input_num = int(input_str)
            if input_num in [1, 2, 3, 4, 5]:
                print("地址:"+list_url[input_num])
                break

