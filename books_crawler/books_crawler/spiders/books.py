import scrapy
from scrapy.http import Request


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        books = response.xpath("//h3/a/@href").extract()
        for book in books:
        	full_url = response.urljoin(book)
        	yield Request(full_url, callback= self.parse_book)

        #get next page
        next_page_url = response.xpath("//li[contains(@class,'next')]/a/@href").extract_first()
        next_page_url = response.urljoin(next_page_url)
        yield Request(next_page_url)
        
    def parse_book(self,response):
       	pass