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
    	url = response.url
    	book_name = response.xpath("//h1/text()").extract_first()
    	price = response.xpath("//p[contains(@class,'price_color')]/text()").extract_first()

    	image = response.xpath("//img/@src").extract_first()
    	image = image.replace("../..","http://books.toscrape.com")
    	
    	rating = response.xpath("//p[contains(@class,'star-rating ')]/@class").extract_first()
    	rating = rating.replace("star-rating ",'')

    	descrption = response.xpath("//div[contains(@id,'product_description')]/following-sibling::p/text()").extract_first()
    	yield{
       		'Title': book_name,
       		'Price': price,
       		'URL' : url,
       		'Image': image,
       		'Descrption': descrption,
       		'Rating':rating
       	} 