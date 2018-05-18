# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['ssb.texas.gov']
    part1 = 'https://www.ssb.texas.gov/news-publications/enforcement-actions-administrative'
    start_urls = ['https://www.ssb.texas.gov/news-publications/enforcement-actions-administrative']

    def parse(self, response):
        for pdf_url in response.xpath('//h4/a/@href'):
            print(pdf_url.extract())
        if '?page' not in response.url:
            yield scrapy.Request(
                url="https://www.ssb.texas.gov/news-publications/enforcement-actions-administrative?page=1",
                callback=self.parse)
        else:
            next_page_url = response.xpath('//li[13][@class="arrow"]/a/@href').extract_first()
            if next_page_url is None:
                next_page_url = response.xpath('//li[14][@class="arrow"]/a/@href').extract_first()
            temp_list = ['https://www.ssb.texas.gov', next_page_url]
            try:
                next_page_url = "".join(temp_list)
                yield scrapy.Request(url=next_page_url, callback=self.parse)
            except TypeError:
                print('All pages have been parse')
