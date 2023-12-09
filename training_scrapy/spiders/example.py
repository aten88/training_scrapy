import scrapy

from training_scrapy.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/',]

    def parse(self, response):
        for quote in response.css('div.quote'):
            data = {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('a.tag::text').getall()
            }
            yield QuoteItem(data)
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
