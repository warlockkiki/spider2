# _*_ coding:utf-8 _*_
import re
# from Article.utils.logintest import get_xsrf2
import tkinter



# root = tkinter.Tk()
# root.maxsize(1200, 1000)
# root.minsize(600, 400)
# root.Label(window,text)
# line = " 12342 收藏"
# rex1 = ".*?(\d.+\d).*"
# matchobj = re.match(rex1,line)
# if re.match(rex1,line):
#     print (matchobj.group(1))
#
# line = "https://www.zhihu.com/question/68621235/answer/265511658"
# rexl = "(.*question/(\d+.*))"
# rexl2 = "(.*zhihu.com/question/(\d+))(/|$).*"
# rexl3 = "(.*question/(\d+).*)"
# value = "查看全部 359 个回答"
# matchobj = re.match(".*?((\d.+\d).|\d{1}).*", value)
#
#
# if re.match(".*?((\d.+\d).|\d{1}).*", value):
#     print(matchobj.group(1))
#     pass
a=['\u200b']
if a[0]=='\u200b':
    print("123")
pass
# xx={'n_c': '1', 'd_c0': '"ACACWIi84wyPTjn6tRJ8jt27igwPRvSkByE=|1514221565"', 'l_cap_id': '"ZjQ4N2MwMTFiNDE2NDBhOWFmZDFiZjM4MGUxODBlMDk=|1514221564|82018056b9ee35c129fa058fe1f0d2b0c5590b8b"', 'l_n_c': '1', 'q_c1': 'c7fa38dbdbfb45cf8dd3cd8a1e0315b1|1514221564000|1514221564000', 'r_cap_id': '"NGE4YmQzNGIwZDc2NGQxZjgxNTYzODY3OGRmMDVjNGY=|1514221564|d2a062a7d6a56d6957b9a68ae67cb4371bdc7396"', 'cap_id': '"M2E5MmI0MjNmNmRlNDg0MWFkYTE4MzkxOTQxM2FjYmU=|1514221564|7cc0a1eaa1f39bede5e9ccc6f4516f570369ce80"', '_xsrf': 'd4399436-477f-46ac-b101-8dddca22e212', 'aliyungf_tc': 'AQAAAHvqLjqAzAsA3chdfCLtEYmT2CuC'}
# for x,y in xx.items():
#     if x=='_xsrf':
#         print(y)
#
# def run_once(f):
#     def wrapper(*args, **kwargs):
#         if not wrapper.has_run:
#             wrapper.has_run = True
#             return f(*args, **kwargs)
#     wrapper.has_run = False
#     return wrapper
#
#
# @run_once
# def my_function(foo, bar):
#     print(foo+bar)
#
# for x in range(1,10):
#     my_function(1,2)

# def get_nums(value):
#     match_re = re.match(".*?((\d.+\d).|\d{1}).*", value)
#     print(match_re.group(1))
# get_nums("查看全部 96 个回答")
# value = "查看全部 4,359 个回答"
# matchobj = re.match(".*?((\d.+\d).|\d{1}).*", value)
#
#
# if re.match(".*?((\d.+\d).|\d{1}).*", value):
#     x=matchobj.group(1).replace(',','').strip()
#     print(x)
#     pass
# def getfirst(value):
#     aa=value[0]
#     print(aa)
# getfirst([123, 123])
# def get_nums(value):
#     match_re = re.match(".*?((\d.+\d).|\d{1}).*", value)
#     if match_re:
#         nums = int(match_re.group(1).replace(',', '').strip())
#         print(nums)
# get_nums('查看全部 96 个回答')
value='查看全部 96 个回答'
if re.match(".*?(\d+).*", value):
    matchobj = re.match(".*?(\d+).*", value)
    print(matchobj.group(1))