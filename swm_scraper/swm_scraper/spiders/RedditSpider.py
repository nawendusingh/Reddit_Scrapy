# -*- encoding: utf-8 -*-
import scrapy

class RedditSpider(scrapy.Spider):
    name = 'RedditSpider'
    allowed_domains = ['https://www.reddit.com/']

    file = open('start_urls.txt', 'r')
    start_urls = [line.rstrip('\n') for line in file]
    file.close()

    custom_settings = {
        'DEPTH_LIMIT': 10
    }

    def parse(self, response):
        titles = response.xpath('//*[@class="_eYtD2XCVieq6emjKBH3m"]/text()').extract()
        upvotes = response.xpath('//*[@class="_1rZYMD_4xY3gRcSS3p8ODO"]/text()').extract()
        number_of_comments = response.xpath('//span[@class="FHCV02u6Cp2zYL0fhQPsO"]/text()').extract()
        timeStamps = response.xpath('//*[@class="_3jOxDPIQ0KaOWpzvSQo-1s"]/text()').extract()

        for (title, upvote, comment, timeStamp) in zip(titles, upvotes, number_of_comments, timeStamps):
            yield {'Post_Title': title, 'Number_of_Upvotes': upvote, 'Number_of_Comments': comment, 'timeStamp': timeStamp}

        next_page = response.xpath('//link[@rel="next"]/@href').extract_first()

        # print(next_page)
        if next_page:
            yield response.follow(next_page, self.parse)
