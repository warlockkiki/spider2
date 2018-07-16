# _*_ coding:utf-8 _*_
import os.path
import requests
import time
from bs4 import BeautifulSoup as BS
import scrapy

try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re

try:
    from PIL import Image
except:
    pass

session = requests.Session()
# session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')

agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 " \
        "Safari/537.36 "
headers = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    'User-Agent': agent
}
# try:
#     session.cookies.load(ignore_discard=True)
# except:
#     print("Cookie 未能加载")




def get_xsrf():
    '''_xsrf 是一个动态变化的参数'''
    index_url = 'https://www.zhihu.com/'
    # 获取登录时需要用到的_xsrf
    index_page = session.get(index_url, headers=headers)
    html = index_page.text
    _xsrf = re.findall('.*name="_xsrf" value="(.*?)"', html)
    print(_xsrf[0])
    #  这里的_xsrf 返回的是一个list
    return _xsrf[0]


def get_index():
    index_url = 'https://www.zhihu.com'
    index_page = session.get(index_url, headers=headers)
    with open("index_page.html", "wb") as f:
        f.write(index_page.text.encode("utf-8"))
    print("ok")


def login(account, password):
    _xsrf = get_xsrf()
    headers["X-Xsrftoken"] = _xsrf
    headers["X-Requested-With"] = "XMLHttpRequest"
    post_url = 'https://www.zhihu.com/login/email'
    postdata = {
        '_xsrf': _xsrf,
        'password': password,
        'email': account
    }
#     response_text = session.post(post_url, data=postdata, headers=header)
#     session.cookies.save()
#
#
# login("779060506@qq.com", "w0417134")


def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha

def isLogin2():
    index_url = "https://www.zhihu.com/settings/profile"
    login_code = session.get(index_url, headers=headers, allow_redirects=False).status_code

    if login_code == 200:
        return True
    else:
        return False
    pass

# def isLogin():
#     # 通过查看用户个人信息来判断是否已经登录
#     url = "https://www.zhihu.com/settings/profile"
#     login_code = session.get(url, headers=headers, allow_redirects=False).status_code
#     if login_code == 200:
#         return True
#     else:
#         return False
#     pass

def zhihu_login(account, password):
    # 知乎登录
    _xsrf = get_xsrf()
    headers["X-Xsrftoken"] = _xsrf
    headers["X-Requested-With"] = "XMLHttpRequest"
    if re.match("^1\d{10}", account):
        print("手机号码登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        postdata = {
            "_xsrf": _xsrf,
            "phone_num": account,
            "password": password,
            "captcha": ""
        }
    else:
        if "@" in account:
            print("邮箱登录 \n")
        else:
            print("你的账号输入有问题，请重新登录")
            return 0
        post_url = 'https://www.zhihu.com/login/email'
        postdata = {
            '_xsrf': _xsrf,
            'password': password,
            'email': account,
            "captcha": ""
        }

    login_page = session.post(post_url, data=postdata, headers=headers)
    login_code = login_page.json()
    if login_code['r'] == 1:
        # 不输入验证码登录失败
        # 使用需要输入验证码的方式登录
        postdata["captcha"] = get_captcha()
        login_page = session.post(post_url, data=postdata, headers=headers)
        login_code = login_page.json()
        print(login_code['msg'])
    # 保存 cookies 到文件，
    # 下次可以使用 cookie 直接登录，不需要输入账号和密码



def loginok():
    session.cookies.save()

# if __name__ == '__main__':
#
#     if isLogin2():
#         print('您已经登录')
#     else:
#
#         zhihu_login("779060506@qq.com", "w0417134")
# zhihu_login(input("zhanghao\n"), input("mima\n"))
# zhihu_login("779060506@qq.com", "w0417134")
# get_index()
# isLogin2()
# get_xsrf()
