# -*- coding: utf-8 -*-
import scrapy


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['opencorporates.com']
    login_url = 'https://opencorporates.com/users/sign_in'
    start_urls = [login_url]

    def parse(self, response):
        token = response.css('input[name="authenticity_token"]::attr(value)').extract_first()
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'utf8': '✓',
                'authenticity_token': token,
                'user[email]': 'ngabomarius@gmail.com',
                'user[password]': 'NTEZIopencorporates30',
            },
            callback=self.after_login,
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return
