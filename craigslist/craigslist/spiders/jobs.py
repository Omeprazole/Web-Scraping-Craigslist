# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://sfbay.craigslist.org/search/sfc/jjj?query=software+engineer&sort=rel']

    def parse(self, response):
        # titles = job.xpath('//a/text()').extract_first()
        # for title in titles:
        #     yield {'Title': title}
        jobs = response.xpath('//p[@class="result-info"]')

        for job in jobs:
            title = job.xpath('a/text()').extract_first()
            address = job.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1]
            relative_url = job.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)

            yield Request(absolute_url, callback=self.parse_page, meta={'URL':absolute_url, 'Title':title, 'Address':address})

        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)
        yield Request(absolute_next_url, callback=self.parse)

    def parse_page(self, response):
        url = response.meta.get('URL')
        title = response.meta.get('Title')
        address = response.meta.get('Address')
        description = "".join(line for line in response.xpath('//*[@id="postingbody"]/text()').extract()).strip()
        compensation = response.xpath('//p[@class="attrgroup"]/span[1]/b/text()').extract_first()
        employment_type = response.xpath('//p[@class="attrgroup"]/span[2]/b/text()').extract_first()
        yield {'URL': url, 'Title': title, 'Address': address, 'Description': description, 'Compensation': compensation, 'Employment Type':employment_type}


