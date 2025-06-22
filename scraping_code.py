from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time


options = Options()
driver = webdriver.Chrome(service=Service("/Users/sandikamacbook/gan-env/chromedriver"), options=options)


url = "https://www.sociolla.com/218_wardah?tab=products&sort=-review_stats.total_reviews&limit=50"
driver.get(url)
time.sleep(5)


try:
   close_btn = driver.find_element(By.CSS_SELECTOR, "button.s-toast__close")
   close_btn.click()
   print("Pop-up ditutup")
   time.sleep(1)
except:
   print("Pop-up tidak ada atau sudah tertutup")


for i in range(0, 10000, 500):
   driver.execute_script(f"window.scrollTo(0, {i});")
   time.sleep(1.5)


products = driver.find_elements(By.CSS_SELECTOR, "div.product__info")
print("Jumlah produk ditemukan:", len(products))


data = []
for idx, product in enumerate(products, 1):
   try:
       nama = product.find_element(By.CSS_SELECTOR, "p.product__name").text
   except:
       nama = ""
   try:
       brand = product.find_element(By.CSS_SELECTOR, "a.product__brand").text
   except:
       brand = ""
   try:
       link = product.find_element(By.CSS_SELECTOR, "a.product__brand").get_attribute("href")
       if link.startswith("/"):
           link = "https://www.sociolla.com" + link
   except:
       link = ""
   try:
       harga = product.find_element(By.CSS_SELECTOR, "h2.product__price").text
   except:
       harga = ""
   try:
       rating = product.find_element(By.CSS_SELECTOR, "span.product__stars").text
   except:
       rating = ""
   try:
       review = product.find_element(By.CSS_SELECTOR, "span.product__reviews").text
   except:
       review = ""


   data.append([idx, nama, brand, harga, rating, review, link])


df = pd.DataFrame(data, columns=["No", "Nama Produk", "Brand", "Harga", "Rating", "Jumlah Review", "Link Produk"])
df.to_excel("data_scraping.xlsx", index=False)


driver.quit()