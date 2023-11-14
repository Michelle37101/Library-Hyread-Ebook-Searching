# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os
import pathlib
from pydub import AudioSegment
from pydub.playback import play

finished_sound = AudioSegment.from_wav('finished.wav')
finished3_sound = AudioSegment.from_wav('finished3.wav')

#reminder sound
#duration  = 1000 #millisecond
#freq = 300 #Hz

# 打開 txt 檔案(內含全台公共圖書館Hyread網址，可根據需求自行增減)並讀取內容
txt_file = pathlib.Path('Library00.txt')
urls = []
with open(txt_file,'r', encoding='UTF-8') as file:
    urls = file.readlines()  # 讀取所有行並儲存為列表
    urls = [link.strip() for link in urls] # 去除換行符"

# 輸入想要搜尋的書名或關鍵字，可輸入多本書
# 由於本程式僅會開啟第一搜尋結果，建議輸入書名副標
# 如："原子習慣"建議輸入"細微改變帶來巨大成就的實證法則";
Booklist = ["細微改變帶來巨大成就的實證法則","蛤蟆先生去看心理師"]


print("----------------------------------------------------------------------------------------------------------------")
print("--------------------------------------------------search start--------------------------------------------------")
print("----------------------------------------------------------------------------------------------------------------")

# Create a new Chrome WebDriver instance
driver = webdriver.Chrome()
# to avoid accidental touch something on webpage, I choose to minimize the window
# or use the following size:
# driver.set_window_size(1000,200)
driver.minimize_window()

# 逐一搜尋每個網頁
for SearchName in Booklist:
    print(SearchName)
    print("     search start")
    
    for Library in urls[:]:
        # 前往指定網址
        driver.get(Library)
        index = str(urls.index(Library))
        # 找到搜尋框，輸入書名\n",
        search_box = driver.find_element(By.ID, "search_input")
        search_box.send_keys(SearchName)
        search_box.send_keys(Keys.ENTER)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "booklist")))
        book_links = driver.find_elements(By.CLASS_NAME, "booklist")

        try:
            link_element = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[3]/div/div/div/div/div[1]/div/section/div[1]/a')
            link_element.click()
            time.sleep(1)
            print("     Find it!", driver.current_url)
            # Open the URL in a new tab
            driver.execute_script("window.open('https://home%s', '_blank');" % index)
            # Switch to the newly opened tab
            driver.switch_to.window(driver.window_handles[-1])
            driver.minimize_window()
        except NoSuchElementException:
            # in case the XPATH changed
            try:
                link_element = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[3]/div/div/div/div/div/div/section/div[1]/a')
                link_element.click()
                time.sleep(1)
                print("     Find it!!", driver.current_url)
                # Open the URL in a new tab
                driver.execute_script("window.open('https://home%s', '_blank')" % index)
                # Switch to the newly opened tab
                driver.switch_to.window(driver.window_handles[-1])
                driver.minimize_window()
            except NoSuchElementException:
                # in case the XPATH changed
                try:
                    link_element = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[3]/div/div/div/div/div/div/section/div[1]/a')
                    link_element.click()
                    time.sleep(1)
                    print("     Find it!!! ", driver.current_url)
                except NoSuchElementException:
                    pass
    print("     search end")
    play(finished_sound)
play(finished3_sound)
print("----------------------------------------------------------------------------------------------------------------")
print("---------------------------------------------------search end--------------------------------------------------")
print("----------------------------------------------------------------------------------------------------------------")

# driver在程式執行完會自動關閉，我沒找到更合適的方法讓網頁持續停留
# 暫時用停1000秒的方法，或者可用break point強制暫停在最後一行
time.sleep(1000)
