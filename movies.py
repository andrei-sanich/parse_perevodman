# -*- coding: utf-8 -*-
import scrapy
import re


class PerevodmanSpider(scrapy.Spider):
    name = 'perevodman'
    start_urls = ['http://perevodman.com/wp-login.php']
    

    def auth(self, response):

        return scrapy.FormRequest.from_response(
            response,
            formid='loginform',
            formdata={
                'log': 'login',
                'pwd': 'password'},
            callback=self.parse)


    def parse(self, response):

        pattern = r'http://perevodman.com/a?m?vo/.+'
        links = response.xpath('//h1/a[2]/@href').extract()
        if links:
            movies = [link for link in links if re.search(pattern, link)]

            for movie_url in movies:
                yield scrapy.Request(movie_url, callback=self.parse_info)
            
            next_page_url = response.xpath('//*[@class="center"]/a[2]/@href').extract_first()
            if next_page_url:
                yield scrapy.Request(next_page_url, callback=self.parse)
            else:
                next_page_url = response.xpath('//*[@class="center"]/a/@href').extract_first()
                yield scrapy.Request(next_page_url, callback=self.parse)


    def parse_info(self, response):
        
        pattern = r'magnet:.+'
        urls = response.xpath('//ul/li/a[1]/@href').extract()                
        title = response.xpath('//h1/a/text()').extract_first()
        translator = response.xpath('//*[@class="comm-star"]/a/text()').extract_first()
        magnet_urls = [url for url in urls if re.search(pattern, url)]
        origin_title = title.split('/')[0].strip()
        tran_title = title.split('/')[1].strip()

        yield {
            'origin_title': origin_title,
            'tran_title': tran_title,
            'translator': translator.strip(),
            'magnet_urls': magnet_urls
            }
