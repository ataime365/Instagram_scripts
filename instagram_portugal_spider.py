from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import time
from random import randint
import os
import csv
from datetime import datetime

class Spider():

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

        self.Ig_file = f"INSTA-{datetime.now().strftime('%y')}{datetime.now().strftime('%m')}-target-urls.csv"
        self.all_influencers_link = [["influencers_links"] ] #A list of lists, #reson for line 86 row = [restaurants]
        self.searchwords = ['#foodportugal', '#foodporto']

        self.url_names = []
        self.driver = driver

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


    def url_scraper(self):
        driver = self.driver
        All_image_links = []

        for searchword in self.searchwords:    
            Searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Search"]')))
            Searchbox.clear()
            Searchbox.send_keys(searchword)
            time.sleep(randint(5,8))
            Searchbox.send_keys(Keys.ENTER)
            Searchbox.send_keys(Keys.ENTER)  #double ENTER
            time.sleep(randint(5,8))
            
            posts = driver.find_element_by_xpath("//span[@class='g47SY ']").text
            print(posts)
            n_scrolls = int(posts.replace(',' , ''))/6
            n_scrolls = round(n_scrolls/5) #Accounting for the 5 scrolls in the second range
            print(n_scrolls)

            li = []   #replace 2 with n_scrolls
            for _ in range(0, n_scrolls): #n_scrolls #do this for 2 scrolls first, if it returns more than 96, run it for the 158 scrools == n_scrolls

                image2 = [] #we need the urls of the images to be in  a list
                for i in range(0, 5):
                    print(i)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(randint(4,9))

                images = driver.find_elements_by_tag_name('a') #A list of links, but we still need to get the image links
                for image in images:
                    image1 = image.get_attribute('href')  #some are videos, we need to get only pictures out so we can use wget to download them

                    if not image1.startswith('https://www.instagram.com/p'):
                        continue
                    image2.append(image1) 

                li.extend(image2)

            All_image_links.extend(li)

        print(All_image_links)


        for url in set(All_image_links):
            try:
                driver.get(url)
                time.sleep(randint(5,8))
                name = driver.find_element_by_xpath("//div[@class='e1e1d']/span/a").get_attribute('href')
                row = [name]
                self.all_influencers_link.append(row)
            except Exception:
                pass



    def main_func(self):
        driver = self.driver
        self.login()
        self.url_scraper()

        print(self.all_influencers_link)

        with open(self.Ig_file, 'w', encoding='utf-8-sig', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.all_influencers_link) #didn't want to use a for loop here, so we used writerows
        
        driver.quit()

session = Spider()
session.main_func()


