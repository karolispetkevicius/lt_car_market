from typing import Any
import scrapy
from parsel import Selector
from scrapy_crawler.data_processor import process_data
from scrapy.utils.project import get_project_settings
import psycopg2
import pandas as pd

class CarSpider(scrapy.Spider):
    name = "car_spider"
    allowed_domains = ["autogidas.lt"]
    start_urls = ["https://autogidas.lt/skelbimai/automobiliai/"]

    car_brands = [
    #     'AC',
    #     'Acura',
    #     'Aixam',
    # #     'Alfa+Romeo',
    #     'Alpina',
    #     'Asia',
    # #    'Audi',
    #      'Austin',
    #      'Bentley',
         'BMW'
        #  'Buick',
        #  'Cadillac',
        #  'Chevrolet'
        #  'Chrysler',
        #   'Citroen'
        #  'Cupra',
        #  'Dacia'
        #  'Daewoo',
        #  'Daihatsu',
        #  'DFSK',
        #  'Dodge'
        #  'DS+Automobiles',
        #   'Fiat'
        #  'Ford',
        #  'GAZ',
        #  'GMC',
        #  'Honda',
        #  'Hummer',
        #  'Hyundai',
        #  'Infiniti',
        #  'Isuzu',
        #  'Iveco',
        #  'Jaguar',
        #  'Jeep',
        #  'Kia'
    #     'Lada',
    #     'Lancia',
    #     'Land+Rover',
    #     'Landwind',
    #     'Lexus',
    #     'Lincoln',
    #     'LuAZ',
    #     'Man',
    #     'Maserati',
    #     'Mazda',
    #     'Mercedes-Benz',
    #     'MG',
    #     'Microcar',
    #     'MINI',
    #     'Mitsubishi',
    #     'Moskvich',
    #     'Nissan',
    #      'Opel',
    #     'Ora',
    #     'Peugeot',
    #     'Polestar',
    #     'Pontiac',
    #     'Porsche',
    #     'Renault',
    #     'Rolls-Royce',
    #     'Rover',
    #      'Saab'
    #     'Santana',
    #     'Seat',
    #     'Skoda',
    #     'Smart',
    #     'Ssangyong',
    #     'Subaru',
    #     'Suzuki',
    #     'Tata',
    #     'Tesla',
    #     'Toyota',
    #     'Trabant',
    #     'UAZ',
    #     'Volkswagen',
    #     'Volvo',
    #     'Yunlong Motors',
    #     'ZAZ'
     ]

    def start_requests(self):

        for brand in self.car_brands:
            
            page = 1
            url = f"https://autogidas.lt/skelbimai/automobiliai/?f_1[0]={brand}&f_model_14[0]=&f_50=atnaujinimo_laika_asc&page={page}"

            yield scrapy.Request(
                url=url,
                method="GET",
                callback=self.parse,
                meta={'brand': brand} 
            )

    
    def __init__(self, *args, **kwargs):
        super(CarSpider, self).__init__(*args, **kwargs)
        self.data = []  # Initialize an empty list to collect data

        # Get the project settings to use the PostgreSQL credentials
        self.settings = get_project_settings()

        # Connect to PostgreSQL database using settings from settings.py
        self.conn = psycopg2.connect(
            dbname=self.settings['POSTGRES']['dbname'],
            user=self.settings['POSTGRES']['user'],
            password=self.settings['POSTGRES']['password'],
            host=self.settings['POSTGRES']['host'],
            port=self.settings['POSTGRES']['port']
        )
        self.cur = self.conn.cursor()

    def parse(self, response):

        car_listings = response.css('.article-item a::attr(href)').getall()
        car_models = response.css('h2.item-title::text').getall()

        for car_ad_link, car_model in zip(car_listings, car_models):

            full_ad_url = response.urljoin(car_ad_link)
            yield scrapy.Request(url=full_ad_url,
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
            mileage = 0

        gearbox = response.css('.icon.param-gearbox b::text').get()

        car_model = response.meta['car_model']

        self.data.append({
            'brand': response.meta['brand'],
            'model': car_model,
            'title': car_title,
            'price': car_price_int,
            'year': car_year,
            'fuel_type': fuel_type,
            'mileage': mileage,
            'gearbox': gearbox,
            'url': response.url
        })

    def closed(self, reason):

        df = process_data(self.data)
        self.store_data_postgres(df)

    def store_data_postgres(self,df):
        # Define a query for inserting data
        insert_query = """
            INSERT INTO car_listings (brand, model, title, price, year, fuel_type, mileage, gearbox, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING; -- This ensures no error on duplicate URLS
        """

        for _, row in df.iterrows():
            try:
                self.cur.execute(insert_query, (
                    row['brand'],
                    row['model'],
                    row['title'],
                    row['price'],
                    row['year'],
                    row['fuel_type'],
                    row['mileage'],
                    row['gearbox'],
                    row['url']
                ))
                self.conn.commit()  # Commit after each row
            except Exception as e:
                self.conn.rollback()  # Rollback in case of an error
                self.logger.error(f"Failed to insert data into PostgreSQL for row: {row.to_dict()} due to error: {e}")

        self.cur.close()
        self.conn.close()









