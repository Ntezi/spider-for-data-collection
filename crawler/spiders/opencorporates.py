# -*- coding: utf-8 -*-
import scrapy
base_url = 'https://opencorporates.com'
login_url = base_url + '/users/sign_in'
companies_url = base_url + '/companies/rw'
email = 'ngabomarius@gmail.com'
password = 'NTEZIopencorporates30'

class OpencorporatesSpider(scrapy.Spider):
    name = 'opencorporates'
    allowed_domains = ['opencorporates.com']
    start_urls = [login_url, companies_url]

    def parse(self, response):
        # extract the csrf token value
        token = response.css('input[name="authenticity_token"]::attr(value)').extract_first()
        # create a python dictionary with the form values
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'utf8': '✓',
                'authenticity_token': token,
                'user[email]': email,
                'user[password]': password,
            },
            callback=self.parse_companies,
        )

        # yield scrapy.FormRequest(url=self.login_url, formdata=data)


    def parse_companies(self, response):
        self.log('I just visited: ' + response.url)
        for company in response.css('li.company'):
            item = {
                'company_name': company.css('a.company_search_result::text').extract_first(),
                'address': company.css('span.address::text').extract_first(),
            }
            yield item
        # follow pagination link
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            self.log('next page url: ' + next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse_companies)