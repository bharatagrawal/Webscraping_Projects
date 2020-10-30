# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request


class SubjectsSpider(Spider):
    name = 'subjects'
    allowed_domains = ['class-central.com']
    start_urls = (
        'http://www.class-central.com/subjects',
    )

    def __init__(self, subject=None):
        self.subject = subject

    def parse(self, response):
        if self.subject:
            subject_url = response.xpath("//a[contains(@title, '"+self.subject+"')]/@href").extract_first()
            yield Request(response.urljoin(subject_url), callback=self.parse_subject)
        else:
            self.logger.info('Scraping all subjects.')
            subjects = response.xpath("//h3//span[contains(.,'courses')]/parent::a/@href").extract()
            for subject in subjects:
                yield Request(response.urljoin(subject), callback=self.parse_subject)

    def parse_subject(self, response):
        pass
