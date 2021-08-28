from selenium import webdriver
from datetime import datetime
import os
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from random import randint
import csv
import json
import time

class Scraper():

    def __init__(self):

        options = webdriver.ChromeOptions()
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        options.add_argument(f'user-agent={userAgent}')
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        options.add_experimental_option("prefs",prefs)

        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options) 
        driver.maximize_window()

        self.instagram_data = { "influencer_name": None, "follower_count": None, "Influencer_page_url": None} #self.instagram_data is a dictionary
        self.in_file = f"INSTA-{datetime.now().strftime('%y')}{datetime.now().strftime('%m')}-target-urls.csv"
        self.out_file = f"INSTA-{datetime.now().strftime('%y')}{datetime.now().strftime('%m')}-raw-data.csv"

        url_list = []
        with open(self.in_file, 'r', encoding='utf-8-sig') as rad:
            reader = csv.reader(rad)
            for i in reader:
                url_list.append(i[0])

        # Unique URLs
        self.url_list = set(url_list)
        # print(self.url_list)

        self.driver = driver            #keys one side, then append the values
        self.instagram = [list(self.instagram_data.keys())] #changes it from a dictionary to a list and then to a list of lists



    def login(self):
        driver = self.driver
        driver.get('https://www.instagram.com/')
        time.sleep(5)
        username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="username"]'))) 
        password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))

        username.clear()
        password.clear()
        username.send_keys('Splendor_clothing')
        password.send_keys('Indigo89')
        Log_in = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
        time.sleep(5)
        # Not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
        #To escape the Not now notifications pop up

    def wr(self): #This writes the headers
        with open(self.out_file, "w", newline="", encoding='utf-8-sig') as wr:
            writer = csv.writer(wr)
            for r in self.instagram:
                writer.writerow(r)

    def convert_views(self, follower_cnt): #This convets the follower counts to numbers
        if 'k' in follower_cnt:
            followers = float(follower_cnt.replace(',', '').split('k')[0]) * 1000
            return followers
        elif 'm' in follower_cnt:
            followers = float(follower_cnt.replace(',', '').split('m')[0]) * 1000000
            return followers
        else:
            followers = float(follower_cnt.replace(',', ''))
            return followers



    def insta_scraper(self):
        driver = self.driver

        instagram_data = self.instagram_data.copy()
        for name_url in self.url_list:
            if name_url == 'influencers_links':
                continue
            # print(name_url)
            try:
                name_url = name_url.strip()
                driver.get(name_url)
                time.sleep(randint(5,8))
                instagram_data["influencer_name"] = driver.find_element_by_xpath("//div[@class='nZSzR']/h2").text
                follower_count = driver.find_element_by_xpath("//section[@class='zwlfE']/ul/li[2]/a/span").text
                instagram_data["follower_count"] = self.convert_views(follower_count)
                instagram_data["Influencer_page_url"] = name_url
                print(instagram_data["follower_count"])
                
                self.instagram.append(list(instagram_data.values()))

            except Exception:
                pass

        driver.quit()
        self.wr()



    def main_func(self):

        self.login()
        self.insta_scraper()
        print(self.instagram)

session = Scraper()
session.main_func()