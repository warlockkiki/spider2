# -*- coding: utf-8 -*-
from selenium import webdriver

browser = webdriver.Chrome(executable_path="D:/virtual/article/Scripts/chromedriver.exe")

browser.get("https://www.zhihu.com/#signin")
browser.find_element_by_xpath('//div[@class="qrcode-signin-step1"]/div[@class="qrcode-signin-cut-button"]/span').click()
browser.find_element_by_xpath(
    '//div[@class="view view-signin"]/form/div[@class="group-inputs"]/div[@class="account input-wrapper"]/input').send_keys(
    "17621189749")
# browser.find_element_by_css_selector(".view-signin input[name='account']").send_keys("17621189749")
browser.find_element_by_css_selector(".view-signin input[name='password']").send_keys("w0417134")
browser.find_element_by_css_selector(".view-signin button.sign-button").click()
# print(browser.page_source)
# browser.quit()

#设置chromedriver不加载图片
# chrome_opt = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images":2}
# chrome_opt.add_experimental_option("prefs", prefs)