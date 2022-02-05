import scrapy

custom_settings = {
        'CURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['cgutierrez.infor@gmail.com'],
        'FEED_EXPORT_ENCODING': 'utf-8'
    }
    
class QuotesSpider(scrapy.Spider):
    name = 'northfacev3'
    start_urls = [
        "https://www.thenorthface.cl/hombre/"
    ]


    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            precios = kwargs['precios']
            nombre_producto = kwargs['nombre_producto']
        precios.extend(response.xpath('//span[@data-price-type="finalPrice"]/span[@class="price"]/text()').getall())
        nombre_producto.extend(response.xpath('//li[@class="item product product-item"]/div/div/strong/a/text()').getall())

        next_page_button_link = response.xpath('//ul//a[@class="action  next"]/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'precios': precios, 'nombre_producto': nombre_producto})
        else:
            yield{
                'precios': precios,
                'nombre_producto': nombre_producto
            }

    def parse(self, response):
        precios = response.xpath('//span[@data-price-type="finalPrice"]/span[@class="price"]/text()').getall()
        nombre_producto = response.xpath('//li[@class="item product product-item"]/div/div/strong/a/text()').getall()


        next_page_button_link = response.xpath('//ul//a[@class="action  next"]/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'precios': precios, 'nombre_producto': nombre_producto})