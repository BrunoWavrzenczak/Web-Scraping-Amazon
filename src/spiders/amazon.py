import scrapy
from scrapy.loader import ItemLoader

from src.items import AmazonItems
from src.utils.stringpy import str_extract

class AmazonSpider(scrapy.Spider):
    name = 'amazon'

    custom_settings = {
        'FEEDS': { 'data/%(name)s/%(name)s_%(time)s.csv': { 'format': 'csv'}}
    }

    base_url = "https://www.amazon.com.br"

    def start_requests(self):
        # INICIA O CRAWLER
        yield scrapy.Request(
            url= "https://www.amazon.com.br/s?k=placa+de+video&i=computers&rh=n%3A16339926011&dc&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=QUTTF0P2CI5B&qid=1696072152&sprefix=placa+de+video%2Caps%2C84&ref=sr_pg_1", 
            callback=self.pagination
        )

    def pagination(self, response):
        # COLETA CADA PROUTO E PROCESSA
        links=response.xpath("//span[@data-component-type='s-product-image']/a/@href").extract()
        for link in links:
            yield scrapy.Request(
                url= self.base_url + link, 
                callback=self.parse_details,
                meta={"page":  str_extract(response.url, "(?<=&ref=).+$")}
            )   
        
        # VAI PARA PROXIMA PAGINA
        next_url = response.xpath("//a[contains(@class, 'pagination-next')]/@href").extract_first()
        if next_url:
            yield scrapy.Request(
                url= self.base_url + next_url,
                callback=self.pagination
            )   
    
    def parse_details(self, response):
        data = ItemLoader(AmazonItems(), response=response)

        data.add_value("url", response.url)
        data.add_value("page", response.meta["page"])
        data.add_value("price", response.xpath("//div[@id='apex_desktop']//span[@class='a-price-whole']/text()").extract_first())
        data.add_value("title", response.xpath("//span[@id='productTitle']/text()").extract_first())
        data.add_value("rating", response.xpath("//div[@id='averageCustomerReviews']//span[@class='a-icon-alt']/text()").extract_first())
        data.add_value("total_rating", response.xpath("//span[@id='acrCustomerReviewText']/text()").extract_first())
        data.add_value("brand", response.xpath("//a[@id='bylineInfo']/text()").extract_first())
        data.add_value("seller", response.xpath("//a[@id='sellerProfileTriggerId']/text()").extract_first())
        features_bullets=response.xpath("//div[@id='feature-bullets']/ul/li//text()").extract()
        data.add_value("features_bullets", ";".join(features_bullets))

        yield data.load_item()
