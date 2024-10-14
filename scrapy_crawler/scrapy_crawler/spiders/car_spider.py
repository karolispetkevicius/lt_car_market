import scrapy


class CarSpiderSpider(scrapy.Spider):
    name = "car_spider"
    allowed_domains = ["autogidas.lt"]
    start_urls = ["https://autogidas.lt/skelbimai/automobiliai/"]

    car_brands = [
        'AC',
        'Acura',
        'Aixam',
        'Alfa+Romeo',
        'Alpina',
        'Asia',
        'Audi'
        'Austin',
        'Bentley',
        'BMW',
        'Buick',
        'Cadillac',
        'Chevrolet',
        'Chrysler',
        'Citroen',
        'Cupra',
        'Dacia',
        'Daewoo',
        'Daihatsu',
        'DFSK',
        'Dodge',
        'DS+Automobiles',
        'Fiat',
        'Ford',
        'GAZ',
        'GMC',
        'Honda',
        'Hummer',
        'Hyundai',
        'Infiniti',
        'Isuzu',
        'Iveco',
        'Jaguar',
        'Jeep',
        'Kia',
        'Lada',
        'Lancia',
        'Land+Rover',
        'Landwind',
        'Lexus',
        'Lincoln',
        'LuAZ',
        'Man',
        'Maserati',
        'Mazda',
        'Mercedes-Benz',
        'MG',
        'Microcar',
        'MINI',
        'Mitsubishi',
        'Moskvich',
        'Nissan',
        'Opel',
        'Ora',
        'Peugeot',
        'Polestar',
        'Pontiac',
        'Porsche',
        'Renault',
        'Rolls-Royce',
        'Rover',
        'Saab',
        'Santana',
        'Seat',
        'Skoda',
        'Smart',
        'Ssangyong',
        'Subaru',
        'Suzuki',
        'Tata',
        'Tesla',
        'Toyota',
        'Trabant',
        'UAZ',
        'Volkswagen',
        'Volvo',
        'Yunlong Motors',
        'ZAZ'
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

        car_listings = response.css('.article-item')

        for car in car_listings:
            model = car.css('h2.item-title::text').get()
            yield {
                'url':response.url,
                'brand': response.meta['brand'],
                'model': model
            }

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




