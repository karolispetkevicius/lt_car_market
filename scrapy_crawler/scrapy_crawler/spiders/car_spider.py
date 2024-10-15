import scrapy
from parsel import Selector


class CarSpiderSpider(scrapy.Spider):
    name = "car_spider"
    allowed_domains = ["autogidas.lt"]
    start_urls = ["https://autogidas.lt/skelbimai/automobiliai/"]

    car_brands = [
        # 'AC',
        # 'Acura',
        # 'Aixam',
        # 'Alfa+Romeo',
        # 'Alpina',
        # 'Asia',
        'Audi',
        # 'Austin',
        # 'Bentley',
        'BMW'
        # 'Buick',
        # 'Cadillac',
        # 'Chevrolet',
        # 'Chrysler',
        # 'Citroen',
        # 'Cupra',
        # 'Dacia',
        # 'Daewoo',
        # 'Daihatsu',
        # 'DFSK',
        # 'Dodge',
        # 'DS+Automobiles',
        # 'Fiat',
        # 'Ford',
        # 'GAZ',
        # 'GMC',
        # 'Honda',
        # 'Hummer',
        # 'Hyundai',
        # 'Infiniti',
        # 'Isuzu',
        # 'Iveco',
        # 'Jaguar',
        # 'Jeep',
        # 'Kia',
        # 'Lada',
        # 'Lancia',
        # 'Land+Rover',
        # 'Landwind',
        # 'Lexus',
        # 'Lincoln',
        # 'LuAZ',
        # 'Man',
        # 'Maserati',
        # 'Mazda',
        # 'Mercedes-Benz',
        # 'MG',
        # 'Microcar',
        # 'MINI',
        # 'Mitsubishi',
        # 'Moskvich',
        # 'Nissan',
        # 'Opel',
        # 'Ora',
        # 'Peugeot',
        # 'Polestar',
        # 'Pontiac',
        # 'Porsche',
        # 'Renault',
        # 'Rolls-Royce',
        # 'Rover',
        # 'Saab',
        # 'Santana',
        # 'Seat',
        # 'Skoda',
        # 'Smart',
        # 'Ssangyong',
        # 'Subaru',
        # 'Suzuki',
        # 'Tata',
        # 'Tesla',
        # 'Toyota',
        # 'Trabant',
        # 'UAZ',
        # 'Volkswagen',
        # 'Volvo',
        # 'Yunlong Motors',
        # 'ZAZ'
    ]

    def start_requests(self):

        headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        }

        for brand in self.car_brands:
            
            page = 1
            url = f"https://autogidas.lt/skelbimai/automobiliai/?f_1[0]={brand}&f_model_14[0]=&f_50=atnaujinimo_laika_asc&page={page}"

            yield scrapy.Request(
                url=url,
                headers=headers,
                method="GET",
                callback=self.parse,
                meta={'brand': brand} 
            )


    def parse(self, response):
        #self.log(f"Response URL: {response.url}")

        headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        }
        car_listings = response.css('.article-item a::attr(href)').getall()
        car_models = response.css('h2.item-title::text').getall()

        for car_ad_link, car_model in zip(car_listings, car_models):

            full_ad_url = response.urljoin(car_ad_link)
            yield scrapy.Request(url=full_ad_url,
                                headers=headers,
                                callback=self.parse_ad,
                                meta={'brand': response.meta['brand'],
                                'car_model': car_model})



        # Extract the last page number from the paginator
        last_page = response.css('div.paginator a[href*="page="] div.page::text') 

        if last_page:
            last_page_number_str = last_page[-2].get()
            self.log(f"Extracted last page number: {last_page_number_str}")

            last_page_number = int(last_page_number_str)  
            # Determine the current page from the URL
            current_page = int(response.url.split('page=')[-1])
            next_page = current_page + 1

        # Check if the next page exists
        if next_page <= last_page_number:
            next_url = f"https://autogidas.lt/skelbimai/automobiliai/?f_1[0]={response.meta['brand']}&f_model_14[0]=&f_50=atnaujinimo_laika_asc&page={next_page}"
            yield scrapy.Request(url=next_url, callback=self.parse, meta={'brand': response.meta['brand']})

    
    def parse_ad(self, response):

        self.log(f"Scraping ad page: {response.url}")

        car_title = response.css('h1.title::text').get()

        car_price_str = response.css('.item-price-content strong::text').get().replace(" ", "").replace("€", "")
        car_price_int = int(car_price_str)

        car_year_str = response.css('.icon.param-year b::text').get()
        car_year = f"{car_year_str}-01"

        fuel_type = response.css('.icon.param-fuel-type b::text').get()

        mileage_html = response.css('.icon.param-mileage').get()
        if mileage_html:
            mileage_selector = Selector(mileage_html)
            mileage_value = mileage_selector.xpath('//b/text()').get()
            mileage = int(mileage_value.replace(" ","").replace("km",""))
        else:
            mileage = None

        gearbox = response.css('.icon.param-gearbox b::text').get()

        car_model = response.meta['car_model']

        yield {
            'brand': response.meta['brand'],
            'model': car_model,
            'title': car_title,
            'price': car_price_int,
            'year': car_year,
            'fuel_type': fuel_type,
            'mileage': mileage,
            'gearbox': gearbox,
            'url': response.url
        }









