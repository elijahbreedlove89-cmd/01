from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service(r"C:\tools\chromedriver\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.google.com")
print("Title:", driver.title)

driver.quit()
