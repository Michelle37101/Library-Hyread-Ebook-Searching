from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import winsound
import os

#reminder sound
#duration  = 1000 #millisecond
#freq = 300 #Hz

# 打開 txt 檔案並讀取內容
txt_file = os.path.dirname(__file__)+'\\Library00.txt'
urls = []
with open(txt_file,'r', encoding='UTF-16') as file:
    urls = file.readlines()  # 讀取所有行並儲存為列表
    urls = [link.strip() for link in urls] # 去除換行符"

Booklist = ["The Passion Paradox"]
#20231027
#"掌握形塑未來30年","從中央思想到群體思維","無所事事的哲學","無法翻譯的情緒","思辨賽局"
#"小狗錢錢","當代價值投資","機率思考的策略論","交易者的超級心流","5000天後","大人學破局","墮落的人腦"
#"知識複利筆記","峰與谷","不拖延的人生","先吃了那隻","逆轉人生8大關鍵力","健身從深蹲開始"


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
    #winsound.Beep(freq, duration)
    winsound.PlaySound('finished.wav', winsound.SND_FILENAME)
winsound.PlaySound('finished3.wav', winsound.SND_FILENAME)
print("----------------------------------------------------------------------------------------------------------------")
print("---------------------------------------------------search end--------------------------------------------------")
print("----------------------------------------------------------------------------------------------------------------")
time.sleep(1000)