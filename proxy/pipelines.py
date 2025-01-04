# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from proxy.items import ProxyItem


class ProxyPipeline:
    def process_item(self, item: ProxyItem, spider):
        # Map proxy types to file names
        file_mapping = {
            'http': 'http.txt',
            'https': 'https.txt',
            'socks4': 'socks4.txt',
            'socks5': 'socks5.txt',
        }

        # Get the file name based on the proxy type
        file_name = file_mapping.get(item["type"].lower())

        # If the type matches one of the keys, write to the corresponding file
        if file_name:
            with open(file_name, 'a') as file:
                file.write(f'{item["ip"]}:{item["port"]}\n')

        return item
