import time

import pandas as pd
import requests
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = "https://filfox.info/en"
html = requests.get(url).text
print(html)


driver = webdriver.Chrome()
# 打开包含目标HTML的网页
driver.get(url)
while "error" in driver.title.lower():
    driver.get(url)
time.sleep(2)

# xpath1 = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div[7]/div[2]/table/tbody/tr[1]/td[2]/span/span/span/a"
# xpath2 = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div[7]/div[2]/table/tbody/tr[2]/td[2]/span/span/span/a"
xpath1 = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div[7]/div[2]/table/tbody/tr["
xpath2 = "]/td[2]/span/span/span/a"

miners = []

# 使用XPath定位具有特定aria-describedby属性的元素
# element_miner1 = driver.find_element(By.XPATH, xpath1)
# miner1 = element_miner1.text
# print(miner1)  # 应该打印出 "f01697248"
#
# element_miner2 = driver.find_element(By.XPATH, xpath2)
# miner2 = element_miner2.text
# print(miner2)  # 应该打印出 "f01697248"

for i in range(1,11):
    miner_element = driver.find_element(By.XPATH,xpath1+str(i)+xpath2)
    miner = miner_element.text
    miners.append(miner)

print(miners)

miners_list = []
try:
    for miner in miners:
        print(f"miner = {miner}")
        driver.get(f'https://filfox.info/en/address/{miner}')
        while "error" in driver.title.lower():
            driver.get(f'https://filfox.info/en/address/{miner}')
        time.sleep(2)

        xpath_pow = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div[3]/div[2]/div[2]/div/div[1]/p[1]"
        xpath_blocks_total = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div[3]/div[2]/div[2]/div/div[2]/div"
        xpath_rewards_total = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div[3]/div[2]/div[2]/div/div[3]/p[1]"
        xpath_locked = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/p[5]"

        # 使用XPath定位具有特定aria-describedby属性的元素
        element_pow = driver.find_element(By.XPATH, xpath_pow)
        pow = element_pow.text.split(" ")[0]
        print(f"pow = {pow}")

        element_blocks_total = driver.find_element(By.XPATH, xpath_blocks_total)
        blocks_total = element_blocks_total.text.split(":")[1].strip()
        print(f"blocks_total = {blocks_total}")

        element_rewards_total = driver.find_element(By.XPATH, xpath_rewards_total)
        rewards_total = element_rewards_total.text.split(":")[1].strip().split(" ")[0]
        print(f"rewards_total = {rewards_total}")

        element_locked = driver.find_element(By.XPATH, xpath_locked)
        rewards_locked = element_locked.text.split(":")[1].strip().split(" ")[0]
        print(f"rewards_locked = {rewards_locked}")

        xpath_blocks = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div[4]/div[2]/div[2]/div[1]"
        xpath_rewards = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div[4]/div[2]/div[2]/p"
        xpath_lucky = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div[4]/div[2]/div[3]/p[2]"

        element_day_blocks = driver.find_element(By.XPATH, xpath_blocks)
        day_blocks = element_day_blocks.text.split(":")[1].strip()
        print(f"day_blocks = {day_blocks}")

        elemetn_day_rewards = driver.find_element(By.XPATH, xpath_rewards)
        day_rewards = elemetn_day_rewards.text.split(":")[1].strip().split(" ")[0]
        print(f"day_rewards = {day_rewards}")

        element_day_lucky = driver.find_element(By.XPATH, xpath_lucky)
        day_lucky = element_day_lucky.text.split(":")[1].strip()
        print(f"day_lucky = {day_lucky}")

        wait = WebDriverWait(driver, 5)
        lab_week_xpath = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div[4]/div[1]/div/div/label[2]"
        lab_week = wait.until(EC.element_to_be_clickable((By.XPATH, lab_week_xpath)))
        lab_week.click()

        time.sleep(2)
        element_week_blocks = driver.find_element(By.XPATH, xpath_blocks)
        week_blocks = element_week_blocks.text.split(":")[1].strip()
        print(f"week_blocks = {week_blocks}")

        elemetn_week_rewards = driver.find_element(By.XPATH, xpath_rewards)
        week_rewards = elemetn_week_rewards.text.split(":")[1].strip().split(" ")[0]
        print(f"week_rewards = {week_rewards}")

        element_week_lucky = driver.find_element(By.XPATH, xpath_lucky)
        week_lucky = element_week_lucky.text.split(":")[1].strip()
        print(f"week_lucky = {week_lucky}")

        lab_month_xpath = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div[4]/div[1]/div/div/label[3]"
        lab_month = wait.until(EC.element_to_be_clickable((By.XPATH, lab_month_xpath)))
        lab_month.click()

        time.sleep(2)
        element_month_blocks = driver.find_element(By.XPATH, xpath_blocks)
        month_blocks = element_month_blocks.text.split(":")[1].strip()
        print(f"month_blocks = {month_blocks}")

        elemetn_month_rewards = driver.find_element(By.XPATH, xpath_rewards)
        month_rewards = elemetn_month_rewards.text.split(":")[1].strip().split(" ")[0]
        print(f"month_rewards = {month_rewards}")

        element_month_lucky = driver.find_element(By.XPATH, xpath_lucky)
        month_lucky = element_month_lucky.text.split(":")[1].strip()
        print(f"month_lucky = {month_lucky}")

        lab_year_xpath = "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div[4]/div[1]/div/div/label[4]"
        lab_year = wait.until(EC.element_to_be_clickable((By.XPATH, lab_year_xpath)))
        lab_year.click()

        time.sleep(2)
        element_year_blocks = driver.find_element(By.XPATH, xpath_blocks)
        year_blocks = element_year_blocks.text.split(":")[1].strip()
        print(f"year_blocks = {year_blocks}")

        elemetn_year_rewards = driver.find_element(By.XPATH, xpath_rewards)
        year_rewards = elemetn_year_rewards.text.split(":")[1].strip().split(" ")[0]
        print(f"year_rewards = {year_rewards}")

        element_year_lucky = driver.find_element(By.XPATH, xpath_lucky)
        year_lucky = element_year_lucky.text.split(":")[1].strip()
        print(f"year_lucky = {year_lucky}")

        miner_dict = {
            "节点号": miner,
            "总算力": pow,
            "总出块": blocks_total,
            "总奖励": rewards_total,
            "锁仓": rewards_locked,
            "幸运值(天)": day_lucky,
            "幸运值(周)": week_lucky,
            "幸运值(月)": month_lucky,
            "幸运值(年)": year_lucky,
            "出块(天)": day_blocks,
            "出块(周)": week_blocks,
            "出块(月)": month_blocks,
            "出块(年)": year_blocks,
            "奖励(天)": day_rewards,
            "奖励(周)": week_rewards,
            "奖励(月)": month_rewards,
            "奖励(年)": year_rewards,
        }
        miners_list.append(miner_dict)
except Exception as e:
    print(f"异常信息: {e.msg}")
    print("当前页面源码:", driver.page_source[:2000])  # 打印部分页面源码


driver.close()

df = pd.DataFrame(miners_list)
time_now = time.strftime("%Y-%m-%d(%H-%M-%S)",time.localtime())
excel_filename = time_now+"-miners.xlsx"

df.to_excel(excel_filename,index=False,engine="openpyxl")
print(f"数据已成功写入Excel文件：{excel_filename}")
