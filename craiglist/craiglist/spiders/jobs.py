import scrapy

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['newyork.craigslist.org']
    start_urls = ['http://newyork.craigslist.org/search/egr']

    def parse(self, response):
        rows = response.xpath("//li[contains(@class,'result-row')]")
        for row in rows:
        	Title = row.xpath(".//h2/a/text()").extract_first()
        	Date = row.xpath(".//time/@datetime").extract_first()
        	URL = row.xpath(".//h2/a/@href").extract_first()

        	yield scrapy.Request(URL, callback = self.parse_jobData,
        						 meta={'Title': Title,
        							   'Date': Date,
        							   'URL': URL
        							  })
        next_page = response.xpath("//a[contains(@class,'button next')]/@href").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_jobData(self,response):
        Title = response.meta['Title']
        Date = response.meta['Date']
        URL = response.meta['URL']
        Compensation = response.xpath("//p[contains(@class,'attrgroup')]/span[contains(.,'compensation: ')]/b/text()").extract_first()
        Employment_type = response.xpath("//p[contains(@class,'attrgroup')]/span[contains(.,'employment type: ')]/b/text()").extract_first()
        Images =response.xpath("//div[contains(@id,'thumbs')]//@href").extract()
        Description = response.xpath("//section[contains(@id,'postingbody')]/text()").extract()
        yield{
            'Title': Title,
            'Date': Date,
            'URL': URL,
            'Compensation': Compensation,
            'Employment_type': Employment_type,
            'Images': Images,
            'Description': Description
        }