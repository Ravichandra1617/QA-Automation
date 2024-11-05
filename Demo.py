import time
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()

driver.get('https://docs3.regularlabs.com/dummycontent/tutorial/word-lists')

Img = driver.find_elements(By.XPATH, '//*[@id="content-wrapper"]//img')
# content =  driver.find_elements(By.)
if len(Img) > 0:
    print ('Fail  This article has a Image')


else:
    print('Pass')
    driver.implicitly_wait(5)


driver.quit()





