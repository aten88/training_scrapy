import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/',]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('a.tag::text').getall()
            }
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


class MessagesSpider(scrapy.Spider):
    name = 'messages'
    start_urls = ['http://51.250.32.185/',]

    def parse(self, response):
        for message in response.css('div.card-body'):
            yield {
                'author': message.css('strong::text').get(),
                'text': ' '.join(message.css('p::text').getall()).strip(),
                'data': message.css('small::text').get()
            }
        next_page = response.xpath("//a[contains(., 'Следующая')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
