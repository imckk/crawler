# Copyright (c) 2024, Cao Kun
#
# All rights reserved.
#
# This file is licensed under the Open Apache License Version 2.0, January 2004, see LICENCE for details.

import re
import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import pandas as pd

# 对不同时间段的数据文本转化为字典类型
def element_to_dict(element_text):
    # 假设 element_text 是你已经获取的字符串
    lines = element_text.split('\n')  # 按行分割字符串

    # 初始化一个空字典来存储键值对
    element_dict = {}

    # 遍历每一行，提取键值对
    for line in lines:
        # 分割键和值
        if ':' not in line:
            line0 = line
            continue
        if line[0] == ':':
            line = line0+line
        parts = line.split(':')
        if len(parts) == 2:
            key, value = parts
            # 清理空格
            key = key.strip()
            value = value.strip()
            # 添加到字典
            element_dict[key] = value

    return element_dict

# 函数：获取单项数据的函数，如果2秒内获取不到就重新加载网页，循环获取
def crawl_one_data(driver,miner_id,name):
    url = f"https://filfox.info/en/address/{miner_id}"
    driver.get(url)
    html = driver.page_source
    tree = etree.HTML(html)


# 定义Xpath类
class Xpath:
    power = "/html/body/div[1]/div/div/div[1]/div[1]/div/div[3]/div[2]/div[2]/div/div[1]/p[1]/text()"
    blocks_total = "/html/body/div/div/div/div[1]/div[1]/div/div[3]/div[2]/div[2]/div/div[2]/div/text()[2]"
    fil_total = "/html/body/div[1]/div/div/div[1]/div[1]/div/div[3]/div[2]/div[2]/div/div[3]/p[1]/text()"
    fil_locked = "/html/body/div[1]/div/div/div[1]/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/p[5]/text()"
    lucky_value = "/html/body/div/div/div/div[1]/div[1]/div/div[4]/div[2]/div[3]/p[2]/text()[2]"
    blocks = "/html/body/div[1]/div/div/div[1]/div[1]/div/div[4]/div[2]/div[2]/div[1]/text()[2]"
    fil = "/html/body/div[1]/div/div/div[1]/div[1]/div/div[4]/div[2]/div[2]/p/text()"

# 定义Miner类
class Miner:
    def __init__(self, miner_id):
        self.miner_id = miner_id
        self.power = "0.0"
        self.blocks_total = "0"
        self.fil_total = "0.0"
        self.fil_locked = "0.0"
        self.day_lucky_value = "0.0"
        self.day_blocks = "0"
        self.day_fils = "0.0"
        self.week_lucky_value = "0.0"
        self.week_blocks = "0"
        self.week_fils = "0.0"
        self.month_lucky_value = "0.0"
        self.month_blocks = "0"
        self.month_fils = "0.0"
        self.year_lucky_value = "0.0"
        self.year_blocks = "0"
        self.year_fils = "0.0"

    def crawl(self, driver):
        try:
            print(f"miner_id:{self.miner_id}")
            url = f"https://filfox.info/en/address/{self.miner_id}"
            driver.get(url)
            #网页标题出现错误，重新加载网页，直到正常
            title = driver.title
            while "error" in title.lower():
                driver.get(url)
                title = driver.title
            # 获取页面源码
            html = driver.page_source
            tree = etree.HTML(html)
            
            print(f"power = {self.power}")
            self.power = tree.xpath(Xpath.power)[0][:6].strip()
            # TODO 取基础数据，如果拿不到数据，就重新加载网页
            while self.power == "0.0":
                time.sleep(1)
                driver.get(url)
                html = driver.page_source
                tree = etree.HTML(html)
                self.power = tree.xpath(Xpath.power)[0][:6].strip()
    
            self.blocks_total = tree.xpath(Xpath.blocks_total)[0][2:].strip()
            self.fil_total = tree.xpath(Xpath.fil_total)[0][15:24].strip()
            self.fil_locked = tree.xpath(Xpath.fil_locked)[0][17:27].strip()
            
            print(f"power = {self.power}")
            print(f"blocks_total = {self.blocks_total}")
            print(f"fil_total = {self.fil_total}")
            print(f"fil_locked = {self.fil_locked}")

            wait = WebDriverWait(driver, 3)
            selector = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div[4]/div[1]/div/div/label[1]"

            # 等待标签按钮可以点击的时候自动点击
            day_tab = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
            day_tab.click()

            # Wait for the updated element
            updated_selector = "div.mx-8.border.border-background.rounded-sm.p-4"
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, updated_selector)))

            html = driver.page_source
            tree = etree.HTML(html)

            # 获取最近24小时，也就是最近1天的数据
            print(f"day_lucky_value = {self.day_lucky_value}")
            self.day_lucky_value = tree.xpath(Xpath.lucky_value)[0][2:].strip()
            while self.day_lucky_value == "0.0":
                time.sleep(1)
                driver.get(url)
                html = driver.page_source
                tree = etree.HTML(html)
                self.day_lucky_value = tree.xpath(Xpath.lucky_value)[0][2:].strip()
            self.day_blocks = tree.xpath(Xpath.blocks)[0][2:].strip()
            self.day_fils = tree.xpath(Xpath.fil)[0].split(':')[1].split(' ')[1]

            # 获取并保存24小时的出块数据文本
            blocks_xpath = "/html/body/div[1]/div/div/div[1]/div[1]/div/div[4]/div[2]/div[2]/div[1]"
            day_blocks_text = driver.find_element(By.XPATH, blocks_xpath).text

            # 点击第2个标签：7天的标签
            selector = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div[4]/div[1]/div/div/label[2]"
            tab_week = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
            tab_week.click()

            # 等待出块数据的文本发生变化
            wait.until(
                lambda driver: driver.find_element(By.XPATH, blocks_xpath).text != day_blocks_text
            )

            # 取刷新后的网页内容
            html = driver.page_source
            # 解析
            tree = etree.HTML(html)

            while tree.xpath(Xpath.lucky_value) == None:
                time.sleep(1)
                driver.get(url)
                html = driver.page_source
                tree = etree.HTML(html)

            # 获取最近7天也就是1周的数据
            self.week_lucky_value = tree.xpath(Xpath.lucky_value)[0][2:].strip()
            self.week_blocks = tree.xpath(Xpath.blocks)[0][2:].strip()
            self.week_fils = tree.xpath(Xpath.fil)[0].split(':')[1].split(' ')[1]

            print(self.week_lucky_value)
            print(self.week_blocks)
            print(self.week_fils)

            # 获取并保存7天标签的出块数据文本
            week_blocks_text = driver.find_element(By.XPATH, blocks_xpath).text

            # 点击第3个标签：30天的标签
            selector = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div[4]/div[1]/div/div/label[3]"
            tab_month = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
            tab_month.click()

            # 等待出块数据的文本发生变化
            wait.until(
                lambda driver: driver.find_element(By.XPATH, blocks_xpath).text != week_blocks_text
            )

            # 取刷新后的网页内容
            html = driver.page_source
            # 解析
            tree = etree.HTML(html)
            while tree.xpath(Xpath.lucky_value) == None:
                time.sleep(1)
                driver.get(url)
                html = driver.page_source
                tree = etree.HTML(html)

            # 获取最近30天也就是1个月的数据
            self.month_lucky_value = tree.xpath(Xpath.lucky_value)[0][2:].strip()
            self.month_blocks = tree.xpath(Xpath.blocks)[0][2:].strip()
            self.month_fils = tree.xpath(Xpath.fil)[0].split(':')[1].split(' ')[1]

            print(self.month_lucky_value)
            print(self.month_blocks)
            print(self.month_fils)

            # 获取并保存30天标签的出块数据文本
            month_blocks_text = driver.find_element(By.XPATH, blocks_xpath).text

            # 点击第4个标签：1年的标签
            selector = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div[4]/div[1]/div/div/label[4]"
            tab_year = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
            tab_year.click()

            # 等待出块数据的文本发生变化
            wait.until(
                lambda driver: driver.find_element(By.XPATH, blocks_xpath).text != month_blocks_text
            )

            # 取刷新后的网页内容
            html = driver.page_source
            # 解析
            tree = etree.HTML(html)
            while tree.xpath(Xpath.lucky_value) == None:
                time.sleep(1)
                driver.get(url)
                html = driver.page_source
                tree = etree.HTML(html)

            # 获取最近1年的数据
            self.year_lucky_value = tree.xpath(Xpath.lucky_value)[0][2:].strip()
            self.year_blocks = tree.xpath(Xpath.blocks)[0][2:].strip()
            self.year_fils = tree.xpath(Xpath.fil)[0].split(':')[1].split(' ')[1]

            print(self.year_lucky_value)
            print(self.year_blocks)
            print(self.year_fils)

        except Exception as e:
            print(f"Error scraping {self.miner_id}: {e}")
            driver.refresh()
class DataWriter:
    @staticmethod
    def write_to_excel(data_list, filename):
        df = pd.DataFrame(data_list)
        df.to_excel(filename, index=False, engine='openpyxl')
# 主程序
if __name__ == "__main__":
    #谷歌浏览器安装路径
    chrome_driver_path = "C:\\Program Files\\Google\\Chrome\\chromedriver.exe"
    # 浏览器选项
    options = Options()
    # 谷歌浏览器服务
    service = Service(chrome_driver_path)
    # 谷歌浏览器驱动句柄 handle
    driver = webdriver.Chrome(service=service, options=options)
    miners_id = ["f01992032", "f01992563", "f01996719", "f01996817"]
    miners_dict_list = []
    for miner_id in miners_id:
        miner = Miner(miner_id)
        miner.crawl(driver)
        miner_dict = vars(miner)
        miners_dict_list.append(miner_dict)
    todayis = time.strftime("%Y-%m-%d(%H-%M-%S)", time.localtime())
    file_name = "E:\\atoshi\\fildata\\"+todayis+"-miners_data.xlsx."
    DataWriter.write_to_excel(miners_dict_list,file_name)
    print(f'数据已写入Excel文件：{file_name}')
    driver.quit()
