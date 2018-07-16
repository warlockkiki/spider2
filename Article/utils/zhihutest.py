_session = None
favor_data = 100


def get_captcha(self):
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    return captcha_url


def show_or_save_captcha(self, url):
    global _session
    r = _session.get(url, headers=zhihu_login_request.headers, verify=True)
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


def save_cookies(self):
    global _session, path_for
    with open('./' + "cookiefile", 'w')as f:
        json.dump(_session.cookies.get_dict(), f)


def read_cookies(self):
    global _session, path_for
    with open('./' + 'cookiefile')as f:
        cookie = json.load(f)
        _session.cookies.update(cookie)


def start_requests(self):
    global _session
    _session = requests.session()
    if os.path.exists('cookiefile'):
        print('have cookies')
        self.read_cookies()
        # self.get_text(question_url)
        for url in self.start_urls:
            yield Request(url, cookies={'www.zhihu.com': 'true'}, callback=self.parse,
                          headers=zhihu_login_request.headers)

    else:
        self.login()


def login(self):
    print("abc")
    global _session
    global header_data
    global _xsrf
    r = _session.get('https://www.zhihu.com', headers=zhihu_login_request.headers, verify=True)
    self._xsrf = re.findall('.*name="_xsrf" value="(.*?)"', r.text)[0]
    account = input("账号：\n")
    password = input("密码：\n")
    if re.match("^1\d{10}", account):
        print("手机号码登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        postdata = {
            "_xsrf": self._xsrf,
            "phone_num": account,
            "password": password,
            'rememberme': 'true',
            "captcha": self.show_or_save_captcha(self.get_captcha())
        }
    else:
        if re.match("^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$", account):
            print("邮箱登录 \n")
        else:
            print("你的账号输入有问题，请重新登录")
            return 0
        post_url = 'https://www.zhihu.com/login/email'
        postdata = {
            '_xsrf': self._xsrf,
            'password': password,
            'email': account,
            'rememberme': 'true',
            "captcha": self.show_or_save_captcha(self.get_captcha())
        }
    r = _session.post(post_url, data=postdata, headers=zhihu_login_request.headers, verify=True)
    j = r.json()
    c = int(j['r'])
    if c == 0:
        print('sign in successful')

        self.save_cookies()
        # os.remove("code.gif")
    else:
        print('登陆出现问题')

        ###################################################################################3