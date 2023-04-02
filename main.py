from curses import window
from tkinter import *
import csv
import requests
import time
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

#change this driver path
DRIVER_PATH = '/Users/malaikasheikh/python/chromedriver'

title = "None"
website = "None"
phone_no = "None"
address = "None"

def extract_name_website(information_page_tag,driver):
  global title
  global website
  try:
    divs = information_page_tag.find_elements(By.TAG_NAME, "div")
    for div in divs:
      #title
      cc = div.get_attribute("class")
      if(cc=="SPZz6b"):
        h2 = div.find_element(By.TAG_NAME, "h2")
        title = h2.text
      #website
      if(cc=="IzNS7c duf-h"):
        a_tags = div.find_elements(By.TAG_NAME, "a")
        for i in range(len(a_tags)):
           if(a_tags[i].text=="Website"):
                website = a_tags[i].get_attribute("href")
                break
  except Exception as e:
    print(e)

def extract_info(information_page_tags,driver):
  print("Extract information")
  try:
    for i in range(len(information_page_tags)):
      class_c = information_page_tags[i].get_attribute("class")
      attr_id = information_page_tags[i].get_attribute("data-attrid")
      if(class_c == "kp-header"):
        extract_name_website(information_page_tags[i],driver)
        print("WEBSITE: ",website)
        print("TITLE: ",title)
  except Exception as e:
    print(e)

def make_request(q_string):
  try:
    page = 0
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    while (page < 60):
      try:
        url = f"https://www.google.com/search?tbs=lf:1,lf_ui:9&tbm=lcl&q={q_string}#rlfi=start:{page}"
        print(url)
        driver.get(url)
        time.sleep(5)
        a_tags = driver.find_elements(By.XPATH, "//div[@id='rl_ist0']/div[@id='rl_ist0']/div/div[1]/div[3]/div/div/div/div/a[1]")
        print(len(a_tags))
        for a_tag in a_tags:
          a_tag.click()
          time.sleep(3)
          information_page_tags = driver.find_elements(By.XPATH, "//async-local-kp/div/div/div[1]/div/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div")
          extract_info(information_page_tags,driver)
        page = page+20
      except:
        break

  except Exception as e:
    print(e)

def search_result(input_query):
  q = input_query
  q = q.replace(" ","+")
  make_request(q)

search_result("Photovoltaikanlage")