# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors


class ArticlePipeline(object):
    def process_item(self, item, spider):
        return item


# 保存JSON的PIPELINE,自定义
class JsonWithEncodingPipeline(object):
    # 设置初始化时打开JSON文件
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")  # 传入JSON文件ARTICLE.JSON W写入 self.file为需要写入的文件

    # 执行将ITEM写入文件
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"  # ensure_ascii设置False防止中文报错，转换ITEM为DICT
        self.file.write(lines)
        return item

    # 关闭文件
    def spider_closed(self, spider):
        self.file.close()


# 调用scrapy提供的json export导出json文件
class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open('articleexporter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii="False")
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


# 传入数据库
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '1231', 'article_scrapy', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title, url, create_date, fav_nums, url_object_id)
            VALUES (%s,%s,%s,%s,%s) 
        """
        # %s 填充4个值 , comment_nums, tags, content,url_object_id,praise_nums,image_url,image_path
        self.cursor.execute(insert_sql,
                            (item["title"], item["url"], item["create_date"], item["fav_nums"], item["url_object_id"]))
        self.conn.commit()


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    # 通过Twisted将mysql插入变为异步执行
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异步异常


        # 处理异步插入的异常

    def handle_error(self, failure, item, spider):
        print(failure)

    # 执行具体插入
    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        # insert_sql = """
        #             insert into jobbole_article(title, url, create_date, fav_nums, url_object_id)
        #             VALUES (%s,%s,%s,%s,%s)
        #         """
        cursor.execute(insert_sql, params)


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "image_path" in item:
            for ok, value in results:
                image_path = value["path"]
                item["image_path"] = image_path

                return item
        pass


class ElasticsearchPipeline(object):
    # 将数据写入到es中

    def process_item(self, item, spider):
        # 将item转换为es的数据
        item.save_to_es()

        return item
