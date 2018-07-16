# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import re
import scrapy
from apscheduler.jobstores import redis

from scrapy.loader.processors import MapCompose, TakeFirst
import datetime
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from Article.models.es_types import ArticleType
from Article.settings import SQL_DATETIME_FORMAT
from Article.utils.common import extract_num
from elasticsearch_dsl.connections import connections


# redis_cli = redis.StrictRedis()
es = connections.create_connection(ArticleType._doc_type.using)
def extract(value):
    return value.extract()[0]


# def int(value):
#     value = int(value)
#     return value

def create_date(value):
    try:
        create_date = datetime.datetime.strptime(value, "%y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def getfirst(value):
    print(value)
    aa = value
    return aa


def get_nums2(value):
    if value:
        asd = int(re.match(".*?(\d+).*", value).group(1).replace(',', '').strip())
        return asd


def get_nums(value):
    match_re = re.match(".*?((\d.+\d).|\d{1}).*", value)
    if match_re:
        nums = int(match_re.group(1).replace(',', '').strip())
    else:
        nums = 0
    return nums


def do_nothing(value):
    return value


# 自定义itemloader，重写。为了一次性调用TakeFirst函数
class ArticleLoaderFirst(ItemLoader):
    default_output_processor = TakeFirst()


# def gen_suggests(index, info_tuple):
#     #根据字符串生成搜索建议数组
#     used_words = set()
#     suggests = []
#     for text, weight in info_tuple:
#         if text:
#             #调用es的analyze接口分析字符串
#             words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter':["lowercase"]}, body=text)
#             anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"])>1])
#             new_words = anylyzed_words - used_words
#         else:
#             new_words = set()
#
#         if new_words:
#             suggests.append({"input":list(new_words), "weight":weight})
#
#     return suggests
class JobboleArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # MapCompose预处理
    title = scrapy.Field(

    )
    create_date = scrapy.Field(
        input_processor=MapCompose(create_date),
        # output_processor=TakeFirst()
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()  # URL长度
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    image_url = scrapy.Field(
        output_processor=MapCompose(do_nothing)
    )
    image_path = scrapy.Field()  # 封面图本地保存位置
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field()
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into jobbole_article(title, url, create_date, fav_nums)
            VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE content=VALUES(fav_nums)
        """
        params = (self["title"], self["url"], self["create_date"], self["fav_nums"])

        return insert_sql, params

    def save_to_es(self):
        article = ArticleType()
        article.title = self['title']
        article.create_date = self["create_date"]
        article.content = remove_tags(self["content"])
        article.image_url = self["image_url"]
        if "image_path" in self:
            article.image_path = self["image_path"]
        article.praise_nums = self["praise_nums"]
        article.fav_nums = self["fav_nums"]
        article.comment_nums = self["comment_nums"]
        article.url = self["url"]
        article.tags = self["tags"]
        article.meta.id = self["url_object_id"]

        # article.suggest = gen_suggests(ArticleType._doc_type.index, ((article.title,10),(article.tags, 7)))

        article.save()

        # redis_cli.incr("jobbole_count")

        return

    pass


class ZhihuQuestionItem(scrapy.Item):
    # 知乎的问题 item
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    # content = scrapy.Field()
    answer_num = scrapy.Field(
        input_processor=MapCompose(get_nums2)
    )
    # comments_num = scrapy.Field()
    watch_user_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    click_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 插入知乎question表的sql语句 comments_num,comments_num=VALUES(comments_num),, %s, %s
        insert_sql = """
            insert into zhihu_question(zhihu_id, topics, url, title, answer_num,
              watch_user_num, click_num
              , crawl_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE answer_num=VALUES(answer_num), 
              watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)
        """
        zhihu_id = self["zhihu_id"][0]
        topics = ",".join(self["topics"])
        url = self["url"][0]
        title = "".join(self["title"])
        # content = "".join(self["content"])
        answer_num = self["answer_num"][0]
        # if self.comments_num[0]=='\u200b':
        #     comments_num = 0
        # else:
        #     comments_num = extract_num("".join(self["comments_num"]))
        # watch_user_num =self["watch_user_num"][0]
        # click_num = self["click_num"][0]
        watch_user_num = int(self["watch_user_num"][0])
        click_num = int(self["click_num"][0])
        # if len(self["watch_user_num"]) == 2:
        #     watch_user_num = int(self["watch_user_num"][0])
        #     click_num = int(self["watch_user_num"][1])
        # else:
        #     watch_user_num = int(self["watch_user_num"][0])
        #     click_num = 0

        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        params = (zhihu_id, topics, url, title, answer_num,
                  # comments_num,
                  watch_user_num, click_num,
                  crawl_time
                  )

        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    # 知乎的问题回答item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 插入知乎question表的sql语句
        insert_sql = """
            insert into zhihu_answer(zhihu_id, url, question_id, author_id, content, praise_num, comments_num,
              create_time, update_time, crawl_time
              ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              ON DUPLICATE KEY UPDATE content=VALUES(content), comments_num=VALUES(comments_num), praise_num=VALUES(praise_num),
              update_time=VALUES(update_time)
        """

        create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATETIME_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATETIME_FORMAT)
        params = (
            self["zhihu_id"], self["url"], self["question_id"],
            self["author_id"], self["content"], self["praise_num"],
            self["comments_num"], create_time, update_time,
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )

        return insert_sql, params
