from scrapy import Spider, Selector
from scrapy.http import Request, TextResponse
from typing import TypedDict
from proxy.items import ProxyItem

#  _____
# /  _/\\
# | / oo
# \(   _\
#  \  O/
#  /   \
#  ||  ||
#  ||  ||      "Hmmmmmmmm..."
#  ||  || _____ /
#  | \ ||(___  )
# // / \|_)o (  )
# \\ ///|)\_(    )
#  ||   |\ )(    )
#  ||   ) \/(____)_     ___
#  ||   |\___/     `---' `.`.
#  ||   | :   _       .'   ))
#  ||   | `..' `~~~-.'   .'__ _
#  \\  /           '.______  ( (
#  ((___ooO                `._\_\


class Cookies(TypedDict):
    page: int
    anonymity: str


class ProxySpider(Spider):
    name = "proxy_4"
    base_url = "https://proxyhub.me/en/vn-sock4-proxy-list.html"
    cookies = Cookies(page=1, anonymity='all')

    def start_requests(self):
        yield from self.make_request()

    def parse(self, response: TextResponse):
        for row in response.css('table tbody tr'):
            # Remove "http" from proxy_ip
            proxy_ip = str(row.css('td:nth-child(1)::text').get())
            proxy_port = str(row.css('td:nth-child(2)::text').get())
            proxy_type = str(row.css('td:nth-child(3)::text').get())

            item = ProxyItem(ip=proxy_ip, port=int(proxy_port),
                             type=proxy_type.lower())

            yield item

        if self.cookies['page'] < 100:
            self.cookies['page'] += 1
            yield from self.make_request()

    def make_request(self):
        yield Request(self.base_url, cookies=dict(self.cookies), callback=self.parse, dont_filter=True)
