import time

from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd

# xpath常量
xpower = "/html/body/div[1]/div/div/div[1]/div[1]/div/div[3]/div[2]/div[2]/div/div[1]/p[1]/text()"
xblocks_total = "/html/body/div/div/div/div[1]/div[1]/div/div[3]/div[2]/div[2]/div/div[2]/div/text()[2]"
xfil_total = "/html/body/div[1]/div/div/div[1]/div[1]/div/div[3]/div[2]/div[2]/div/div[3]/p[1]/text()"
xfil_locked = "/html/body/div[1]/div/div/div[1]/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/p[5]/text()"

# 通过 etree和 xpath,获取单个数据元的值: power,blocks_total,fil_total,fil_locked
def getDataByXpath(tree,xph):
    res_data = ""
    if xph == xpower:
        if len(tree.xpath(xpower)) != 0:
            res_data = tree.xpath(xpower)[0][:6].strip()
    elif xph == xblocks_total:
        if len(tree.xpath(xblocks_total)) != 0:
            res_data = tree.xpath(xblocks_total)[0][2:].strip()
    elif xph == xfil_total:
        if len(tree.xpath(xfil_total)) != 0:
            res_data = tree.xpath(xfil_total)[0][15:24].strip()
    elif xph == xfil_locked:
        if len(tree.xpath(xfil_locked)) != 0:
            res_data = tree.xpath(xfil_locked)[0][17:27].strip()
    return res_data


# 标签常量：天，周，月，年
day_label = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div[4]/div[1]/div/div/label[1]"
week_label = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div[4]/div[1]/div/div/label[2]"
month_label = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div[4]/div[1]/div/div/label[3]"
year_label = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div[4]/div[1]/div/div/label[4]"

# 把element text 转换为字典
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

    # 现在可以从字典中获取 'Blocks Mined' 的值
    return element_dict

# 通过label,返回一个包含三个数据的字典
def getDataByElement(driver,selector,blocks_text):
    res_data = {}

    blocks_xpath = "/html/body/div[1]/div/div/div[1]/div[1]/div/div[4]/div[2]/div[2]/div[1]"

    # 网页加载过程中，等待标签按钮可以点击的时候，自行点击
    wait = WebDriverWait(driver, 20)
    tab = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
    tab.click()

    # Wait for the updated element
    updated_selector = "div.mx-8.border.border-background.rounded-sm.p-4"
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, updated_selector)))

    # 等待出块数据的文本发生变化
    wait.until(
        lambda driver: driver.find_element(By.XPATH, blocks_xpath).text != blocks_text
    )

    blocks_text = driver.find_element(By.XPATH, blocks_xpath).text

    element_xpath = "/html/body/div/div/div/div[1]/div[1]/div/div[4]/div[2]"
    element_text = driver.find_element(By.XPATH, element_xpath).text
    if not element_text:
        return res_data
    ele_dict = element_to_dict(element_text)

    res_data["block_text"] = blocks_text
    res_data["lucky"] = ele_dict['Lucky Value']
    res_data["blocks"] = ele_dict['Blocks Mined']
    res_data["fil"] = ele_dict['Rewards (Ratio)'].split(' ')[0]

    return res_data


class Miner:
    def __init__(self, miner_id):
        self.miner_id = miner_id
        self.power = ""
        self.blocks_total = ""
        self.fil_total = ""
        self.fil_locked = ""
        self.day_lucky = ""
        self.day_blocks = ""
        self.day_fil = ""
        self.week_lucky = ""
        self.week_blocks = ""
        self.week_fil = ""
        self.month_lucky = ""
        self.month_blocks = ""
        self.month_fil = ""
        self.year_lucky = ""
        self.year_blocks = ""
        self.year_fil = ""
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

            html = driver.page_source
            tree = etree.HTML(html)

            # 获取power
            self.power = getDataByXpath(tree,xpower)
            while self.power == "":
                driver.get(url)
                html = driver.page_source
                tree = etree.HTML(html)
                self.power = getDataByXpath(tree, xpower)
            print(f"self.power = {self.power}")

            # 获取blocks_total
            self.blocks_total = getDataByXpath(tree, xblocks_total)
            while self.blocks_total == "":
                driver.get(url)
                html = driver.page_source
                tree = etree.HTML(html)
                self.blocks_total = getDataByXpath(tree, xblocks_total)

            print(f"self.blocks_total = {self.blocks_total}")
            # 获取fil_total
            self.fil_total = getDataByXpath(tree, xfil_total)
            while self.fil_total == "":
                driver.get(url)
                html = driver.page_source
                tree = etree.HTML(html)
                self.fil_total = getDataByXpath(tree, xfil_total)

            print(f"self.fil_total = {self.fil_total}")
            # 获取fil_locked
            self.fil_locked = getDataByXpath(tree, xfil_locked)
            while self.fil_locked == "":
                driver.get(url)
                html = driver.page_source
                tree = etree.HTML(html)
                self.fil_locked = getDataByXpath(tree, xfil_locked)

            print(f"self.fil_locked = {self.fil_locked}")

            # 获取24小时的 lucky,blocks fil
            block_text = ""
            day_data = getDataByElement(driver,day_label,block_text)
            while len(day_data) == 0:
                driver.get(url)
                day_data = getDataByElement(driver,day_label,block_text)
            self.day_lucky = day_data["lucky"]
            self.day_blocks = day_data["blocks"]
            self.day_fil = day_data["fil"]
            block_text = day_data["block_text"]

            print(f"self.day_lucky = {self.day_lucky}")
            print(f"self.day_blocks = {self.day_blocks}")
            print(f"self.day_fil = {self.day_fil}")


            # 获取1周的 lucky,blocks fil
            week_data = getDataByElement(driver,week_label,block_text)
            while len(week_data) == 0:
                driver.get(url)
                week_data = getDataByElement(driver,week_label,block_text)
            self.week_lucky = week_data["lucky"]
            self.week_blocks = week_data["blocks"]
            self.week_fil = week_data["fil"]
            block_text = week_data["block_text"]

            print(f"self.week_lucky = {self.week_lucky}")
            print(f"self.week_blocks = {self.week_blocks}")
            print(f"self.week_fil = {self.week_fil}")


            # 获取1个月的 lucky,blocks fil
            month_data = getDataByElement(driver,month_label,block_text)
            while len(month_data) == 0:
                driver.get(url)
                month_month = getDataByElement(driver,month_label,block_text)
            self.month_lucky = month_data["lucky"]
            self.month_blocks = month_data["blocks"]
            self.month_fil = month_data["fil"]
            block_text = month_data["block_text"]

            print(f"self.month_lucky = {self.month_lucky}")
            print(f"self.month_blocks = {self.month_blocks}")
            print(f"self.month_fil = {self.month_fil}")

            # 获取1年的 lucky,blocks fil
            year_data = getDataByElement(driver,year_label,block_text)
            while len(month_data) == 0:
                driver.get(url)
                year_data = getDataByElement(driver,year_label,block_text)
            self.year_lucky = year_data["lucky"]
            self.year_blocks = year_data["blocks"]
            self.year_fil = year_data["fil"]

            print(f"self.year_lucky = {self.year_lucky}")
            print(f"self.year_blocks = {self.year_blocks}")
            print(f"self.year_fil = {self.year_fil}")

        except Exception as e:
            print(f"Error crawling  {self.miner_id}: {e}")

class DataWriter:
    @staticmethod
    def write_to_excel(data_list, filename):
        df = pd.DataFrame(data_list)
        df.to_excel(filename, index=False, engine='openpyxl')


if __name__ == "__main__":
    # #谷歌浏览器安装路径
    # chrome_driver_path = "C:\\Program Files\\Google\\Chrome\\chromedriver.exe"
    # # 浏览器选项
    # options = Options()
    # # 谷歌浏览器服务
    # service = Service(chrome_driver_path)
    # 谷歌浏览器驱动句柄 handle
    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome()
    miners_id = ["f01992032", "f01992563", "f01996719", "f01996817"]
    miners_dict_list = []
    for miner_id in miners_id:
        miner = Miner(miner_id)
        miner.crawl(driver)
        miner_dict = vars(miner)
        miners_dict_list.append(miner_dict)
    time_now = time.strftime("%Y-%m-%d(%H-%M-%S)", time.localtime())
    file_name = "E:\\atoshi\\fildata\\"+time_now+"-miners_data.xlsx."
    DataWriter.write_to_excel(miners_dict_list,file_name)
    print(f'数据已写入Excel文件：{file_name}')
    driver.quit()













