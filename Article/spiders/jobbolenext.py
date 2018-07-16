# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse
from Article.items import JobboleArticleItem, ArticleLoaderFirst
from Article.utils.common import get_md5
from scrapy.loader import ItemLoader
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

# import urlparse PY2写法

class JobbolenextSpider(scrapy.Spider):
    name = 'jobbolenext'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts']
    # handle_httpstatus_list = [404]
    # def __init__(self, **kwargs):
    #     self.fail_urls = []
    #     dispatcher.connect(self.handle_spider_closed, signals.spider_closed)
    #
    # def handle_spider_closed(self, spider, reason):
    #     self.crawler.stats.set_value("failed_urls", ",".join(self.fail_urls))
    def parse(self, response):
        # 提取页面所有URL
        post_nodes = response.xpath('//div[@class="post floated-thumb"]/div[@class="post-thumb"]/a')
        # post_urls = response.css("#archive div.floated-thumb .post-thumb a::attr(href)").extract()
        for post_node in post_nodes:
            # print(post_node)
            image_url = post_node.xpath("img/@src").extract()[0]
            post_url = post_node.xpath("@href").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"image_url": image_url},
                          callback=self.parse_dateil)  # 获取的URL不一定含有主域名，
            # urljoin函数完成URL拼接，
            # yield 把REQUEST交给scrapy进行下载

            # 提取下一页交给SCRAPY进行下载
        next_url = response.xpath('//div[@class="navigation margin-20"]/a[@class="next page-numbers"]/@href').extract()
        print(next_url)
        if next_url:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)

    def parse_dateil(self, response):
        # 提取页面具体字段
        image_url = response.meta.get("image_url", "")  # response.meta["image_url"]   get方法不报错,默认值为空
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].replace("·",
        #                                                                                                     "").strip()
        # praise_nums = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0]
        # fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        # # print(post_url)
        # match_re = re.match(".*?((\d.+\d).|\d{1}).*", fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        # comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        # match_re = re.match(".*?((\d.+\d).|\d{1}).*", comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = ",".join(tag_list)
        # content = response.xpath("//div[@class='entry']").extract()[0].strip()
        #
        # article_item = JobboleArticleItem()
        # article_item["url_object_id"] = get_md5(response.url)
        # article_item["title"] = title
        # article_item["url"] = response.url
        # # try:
        # #     create_date = datetime.datetime.strptime(create_date, "%y/%m/%d").date()
        # # except Exception as e:
        # #     create_date = datetime.datetime.now().date()
        # article_item["create_date"] = create_date
        # article_item["praise_nums"] = praise_nums
        # article_item["image_url"] = [image_url]
        # article_item["fav_nums"] = fav_nums
        # article_item["comment_nums"] = comment_nums
        # article_item["tags"] = tags
        # article_item["content"] = content

        # 通过item loader加载item
        # item_loader = ItemLoader(item=JobboleArticleItem(), response=response)
        # 通过自定义item loader加载item
        item_loader = ArticleLoaderFirst(item=JobboleArticleItem(), response=response)
        item_loader.add_xpath("title", "//div[@class='entry-header']/h1/text()")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_xpath("create_date", "//p[@class='entry-meta-hide-on-mobile']/text()")
        item_loader.add_value("image_url", [image_url])
        item_loader.add_xpath("praise_nums", "//span[contains(@class, 'vote-post-up')]/h10/text()")
        item_loader.add_xpath("fav_nums", "//span[contains(@class, 'bookmark-btn')]/text()")
        item_loader.add_xpath("comment_nums", "//a[@href='#article-comment']/span/text()")
        item_loader.add_xpath("tags", "//p[@class='entry-meta-hide-on-mobile']/a/text()")
        item_loader.add_xpath("content", "//div[@class='entry']")

        article_item = item_loader.load_item()
        yield article_item
        pass
