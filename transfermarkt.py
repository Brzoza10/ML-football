# -*- coding: utf-8 -*-
import scrapy

class TransfermarktSpider(scrapy.Spider):
    name = 'transfermarkt'
    allowed_domains = ['transfermarkt.pl']
    start_urls = ['https://www.transfermarkt.pl/premier-league/startseite/wettbewerb/GB1']

    def parse(self, response):
        years = response.xpath('//select[@name="saison_id"]/option/@value').extract()
        start = 'https://www.transfermarkt.pl/premier-league/startseite/wettbewerb/GB1/plus/?saison_id=%s'
        urls = list()
        for year in years:
            urls.append(start % year)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_application)

    def parse_application(self, response):
        teams = response.xpath('//td[@class="hauptlink no-border-links show-for-small show-for-pad"]/a/text()').extract()
        values = response.xpath('//td[@class="rechts hide-for-small hide-for-pad"]/a/text()').extract()
        season = response.xpath('//h2[@class="table-header"]/text()').extract_first().split(" ")[-1]
        for team, value in zip(teams,values):
            if value != '-':
                yield{'Season':[season], 'Team': team, 'Value': value}

