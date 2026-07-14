from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
import time

driver = webdriver.Chrome()
driver.get("http://www.python.com")
titulo = driver.find_element(By.TAG_NAME, 'title')
print(titulo.text)