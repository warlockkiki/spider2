# -*- coding: utf-8 -*-
import sys, re, os, scrapy, time, urllib, pickle, json, http.cookiejar, requests, datetime
from scrapy import Selector, Request, signals
from bs4 import BeautifulSoup as BS
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from Article.items import ZhihuAnswerItem, ZhihuQuestionItem
from Article.utils import zhihu_login_request, do_once
from scrapy.http import Request, FormRequest
from selenium.webdriver.support.ui import WebDriverWait
from scrapy.xlib.pydispatch import dispatcher
import tkinter
from tkinter.ttk import *
from tkinter import *

try:
    from urllib import parse, request
except:
    import urlparse
try:
    from PIL import Image
except:
    pass
try:
    import cookielib
except:
    import http.cookiejar as cookielib
from selenium import webdriver

from bs4 import BeautifulSoup

# cookieJar = cookielib.CookieJar()
# opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookieJar))


session = requests.Session()
session.cookies = http.cookiejar.LWPCookieJar("cookiefile")

custom_settings = {
    "COOKIES_ENABLED": True
}


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com']
    start_answer_url = 'https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}'

    # def __init__(self):
    #     self.browser = webdriver.Chrome(executable_path="D:/virtual/article/Scripts/chromedriver.exe")
    #     super(ZhihuSpider).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    # 
    # def spider_closed(self, spider):
    #     print("spider closed")
    #     self.browser.close()

    def parse(self, response):
        print("回调成功")
        """
                提取出html页面中的所有url 并跟踪这些url进行一步爬取
                如果提取的url中格式为 /question/xxx 就下载之后直接进入解析函数
        """
        # all_url = response.xpath('//li[@class="zm-topic-organize-item"]/a/@href')
        # all_urls = response.xpath('//a[@class="question_link"]/@href').extract()
        all_urls = response.xpath('//a/@href').extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]

        for url in all_urls:
            # print(url)
            match_obj = re.match("(.*question/(\d+).*)", url)
            if match_obj:
                # 如果提取到question相关的页面则下载后交由提取函数进行提取
                request_url = match_obj.group(1)
                yield scrapy.Request(request_url, headers=zhihu_login_request.headers, callback=self.parse_question)
                # else:
                # 如果不是question页面则直接进一步跟踪
                # yield scrapy.Request(real_url, headers=zhihu_login_request.headers, callback=self.parse)
            pass
        pass

    def parse_question(self, response):
        match_obj = re.match("(.*question/(\d+).*)", response.url)
        if 'answer' in response.url:
            if match_obj:
                question_id = int(match_obj.group(2))
            # title_A = response.xpath('//div[@class="QuestionHeader-main"]/h1/text()')
            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_xpath("title", '//div[@class="QuestionHeader-main"]/h1/text()')
            # item_loader.add_xpath("content", '//span[@class="RichText"]/text()')
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            # answer_num_C = response.xpath('//div[@class="Card"]/a/text()')
            item_loader.add_xpath("answer_num",'//div[@class="Question-mainColumn"]/div[1]/a/text()')
            # item_loader.add_xpath("comments_num", '//div[@class="QuestionHeader-Comment"]/button/span/text()')
            item_loader.add_xpath("click_num",
                                  '//div[@class="NumberBoard QuestionFollowStatus-counts NumberBoard--divider"]/div[@class="NumberBoard-item"]/div[@class="NumberBoard-itemInner"]/strong[@class="NumberBoard-itemValue"]/text()')
            item_loader.add_xpath("topics", '//a[@class="TopicLink"]/div[@class="Popover"]/div/text()')
            item_loader.add_xpath("watch_user_num",
                                  '//div[@class="NumberBoard QuestionFollowStatus-counts NumberBoard--divider"]/button[@class="Button NumberBoard-item Button--plain"]/div[@class="NumberBoard-itemInner"]/strong[@class="NumberBoard-itemValue"]/text()')
            question_item = item_loader.load_item()
        else:
            if match_obj:
                question_id = int(match_obj.group(2))
            # title_A = response.xpath('//div[@class="QuestionHeader-main"]/h1/text()')
            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_xpath("title", '//div[@class="QuestionHeader-main"]/h1/text()')
            # item_loader.add_xpath("content", '//span[@class="RichText"]/text()')
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            # answer_num_C = response.xpath('//div[@class="Card"]/a/text()')
            item_loader.add_xpath("answer_num",
                                  '//div[@class="Card"]/div[@class="List"]/div[@class="List-header"]/h4[@class="List-headerText"]/span/text()')
            # item_loader.add_xpath("comments_num", '//div[@class="QuestionHeader-Comment"]/button/span/text()')
            item_loader.add_xpath("click_num",
                                  '//div[@class="NumberBoard QuestionFollowStatus-counts NumberBoard--divider"]/div[@class="NumberBoard-item"]/div[@class="NumberBoard-itemInner"]/strong[@class="NumberBoard-itemValue"]/text()')
            item_loader.add_xpath("topics", '//a[@class="TopicLink"]/div[@class="Popover"]/div/text()')
            item_loader.add_xpath("watch_user_num",
                                  '//div[@class="NumberBoard QuestionFollowStatus-counts NumberBoard--divider"]/button[@class="Button NumberBoard-item Button--plain"]/div[@class="NumberBoard-itemInner"]/strong[@class="NumberBoard-itemValue"]/text()')
            question_item = item_loader.load_item()
        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), headers=zhihu_login_request.headers,
                             callback=self.parse_answer)
        yield question_item
        pass

    def parse_answer(self, reponse):
        # 处理question的answer
        ans_json = json.loads(reponse.text)
        is_end = ans_json["paging"]["is_end"]
        next_url = ans_json["paging"]["next"]

        # 提取answer的具体字段
        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["praise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, headers=zhihu_login_request.headers, callback=self.parse_answer)

    def start_requests(self):
        # global session
        # session = requests.session()
        # session.cookies = http.cookiejar.LWPCookieJar("cookiefile")
        # if os.path.exists('cookiefile'):
        #     self.read_cookies()
        #     return [
        #         scrapy.Request('https://www.zhihu.com/#signin',
        #                        headers=zhihu_login_request.headers
        #                        )]
        # else:
        return [
            scrapy.Request('https://www.zhihu.com/signin',
                           headers=zhihu_login_request.headers,
                           callback=self.login)]
        # def reg(self):
        # global zhanghao,mima,yanzhengma
        # zhanghao=e1.get()
        # mima=e2.get()
        # yanzhengma=e3.get()

    def login(self, response):
        global session
        global _xsrf
        # if zhihu_login_request.isLogin2():
        #     print("已经登录")
        #     for url in self.start_urls:
        #         yield scrapy.Request(url, meta={'cookiejar': True}, dont_filter=True,
        #                              headers=zhihu_login_request.headers, callback=self.parse)
        # else:
        if 1:
            # soup = BeautifulSoup(response.content, "html.parser")
            # xsrf = soup.find('input', attrs={"name": "_xsrf"}).get("value")
            # root = tkinter.Tk()
            # root.maxsize(1200, 1000)
            # root.minsize(600, 400)
            # print(session)
            print("没有登录")
            # p = session.post("http://example.com", {'user': '17621189749', 'password': 'w0417134'})
            # print('cookies', requests.utils.dict_from_cookiejar(session.cookies))
            # _xsrf = response.css("form input[name='_xsrf']::attr('value')").extract_first("")
            session = requests.Session()
            session.cookies.get_dict()
            {}
            response = session.get('https://www.zhihu.com', headers=zhihu_login_request.headers, verify=True)
            zx = session.cookies.get_dict()
            for x, y in zx.items():
                if x == '_xsrf':
                    print(y)

                    # y = int(y.encode("utf-8"))
                    _xsrf = y
            # html = response.body
            # r = session.get('https://www.zhihu.com', headers=zhihu_login_request.headers, verify=True)

            # _xsrff = re.findall('.*name="_xsrf" value="(.*?)"',
            #                     r.text,
            #                     # html
            #                     )
            # _xsrff = re.match('.*name="_xsrf" value="(.*?)"', html, re.DOTALL)
            # _xsrf = _xsrff[0]
            # global zhanghao, mima, yanzhengma
            # global e1,e2
            # l = Label(root, text="账号:")
            # l.grid(row=1, column=1, sticky=W)
            # e1 = Entry(root)
            # e1.grid(row = 1,column=2,sticky=E)
            # l2 = Label(root, text="密码:")
            # l2.grid(row=2, column=1, sticky=W)
            # e2 = Entry(root)
            # e2['show']='*'
            # e2.grid(row=2, column=2, sticky=E)
            # l3 = Label(root, text="账号:")
            # l3.grid(row=3, column=1, sticky=W)
            # global e3
            # e3 = Entry(root)
            # e3.grid(row=3, column=2, sticky=E)
            # b = Button(root,text="登录",command=self.reg)
            # b.grid(row=4, column=2, sticky=E)
            # account = zhanghao
            # password = mima
            # tkinter.mainloop()
            # account = input("账号：\n")
            # password = input("密码：\n")
            account = '17621189749'
            password = 'w0417134'
            if _xsrf:
                if re.match("^1\d{10}", account):
                    print("手机号码登录")
                    post_url = "https://www.zhihu.com/login/phone_num"
                    postdata = {
                        "_xsrf": _xsrf,
                        "phone_num": account,
                        "password": password,
                        'rememberme': 'true',
                        "captcha": ""
                    }
                else:
                    if re.match("^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$", account):
                        print("邮箱登录 \n")
                    else:
                        print("你的账号输入有问题，请重新登录")
                        return 0
                    post_url = 'https://www.zhihu.com/login/email'
                    postdata = {
                        '_xsrf': _xsrf,
                        'password': password,
                        'email': account,
                        'rememberme': 'true',
                        "captcha": ""
                    }
                t = str(int(time.time() * 1000))
                captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
                # r = session.get(captcha_url, headers=zhihu_login_request.headers)
                yield scrapy.Request(captcha_url, headers=zhihu_login_request.headers,
                                     meta={"post_data": postdata, "post_url": post_url, },
                                     callback=self.login_after_captcha)

    def login_after_captcha(self, response):
        with open("captcha.jpg", "wb") as f:
            f.write(response.body)
            f.close()
        from PIL import Image
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            pass

        # captcha = yanzhengma

        captcha = input("输入验证码\n>")
        post_data = response.meta.get("post_data", {})
        post_data["captcha"] = captcha
        post_url = response.meta.get("post_url", {})

        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=zhihu_login_request.headers,
            callback=self.check_login
        )]

    def check_login(self, response):
        # 验证服务器的返回数据判断是否成功
        text_json = json.loads(response.text)
        # if "msg" in text_json and text_json["msg"] == "登录成功":
        for url in self.start_urls:
            yield scrapy.Request(url,
                                 dont_filter=True, headers=zhihu_login_request.headers,
                                 )

    def save_cookies(self):
        global session, path_for
        with open('./' + "cookiefile", 'w')as f:
            json.dump(session.cookies.get_dict(), f)

    def read_cookies(self):
        global session, path_for
        with open('./' + 'cookiefile')as f:
            cookie = json.load(f)
            session.cookies.update(cookie)


pass
