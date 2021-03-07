import scrapy
from scrapy.http import HtmlResponse
from GoodsFind.items import GoodsfindItem


class CitilinkruSpider(scrapy.Spider):
    name = 'citilinkru'
    allowed_domains = ['citilink.ru']
    start_urls = ['https://www.citilink.ru/catalog/holodilniki/?f=discount.price1_20%2C3415_323dvukhkamernyy%2C10413_323vd1kholodila2nomd1id1morozila2nomd1otdelenii']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@class='PaginationWidget__arrow PaginationWidget__arrow_right']/@href").extract_first()
        goods_links = response.xpath("//div[@class='product_data__gtm-js product_data__pageevents-js ProductCardHorizontal js--ProductCardInListing js--ProductCardInWishlist']/a/@href").extract()
        for link in goods_links:
            yield response.follow(link, callback=self.good_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            return

    def good_parse(self, response:HtmlResponse):
        item_name = response.xpath("//h1[@class='Heading Heading_level_1 ProductHeader__title']/text()").extract_first()
        item_price = response.xpath("//div[@class='ProductPrice ProductPrice_default ProductHeader__price-default']//text()").extract()[0]
        yield GoodsfindItem(name=item_name, price=item_price, href= response.url , site=self.name )
