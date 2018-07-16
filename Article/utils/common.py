import hashlib,re


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()  # md5摘要生成

def extract_num(text):
    match_re = re.match(".*?((\d.+\d).|\d{1}).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums

# if __name__ == "__main__":
#     print(get_md5("http://www.acfun.cn/"))
#     pass
