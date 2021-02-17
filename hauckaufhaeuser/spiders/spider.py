import scrapy

from scrapy.loader import ItemLoader
from ..items import HauckaufhaeuserItem
from itemloaders.processors import TakeFirst


class HauckaufhaeuserSpider(scrapy.Spider):
	name = 'hauckaufhaeuser'
	start_urls = ['https://www.hauck-aufhaeuser.com/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="x-subtitle"]')
		for post in post_links:
			date = post.xpath('./a/span[2]//text()').get()
			link = post.xpath('./a/@href').get()
			yield response.follow(link, self.parse_post, cb_kwargs=dict(date=date))

		next_page = response.xpath('//div[@class="pagination pagination__posts"]/ul/li[@class="next"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)



	def parse_post(self, response, date):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="ce-bodytext"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=HauckaufhaeuserItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
