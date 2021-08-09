import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from io import BytesIO 
import lxml.html 
from PIL import Image
import pytesseract 
import lxml.html
import urllib.request as urllib2
import pprint
import http.cookiejar as cookielib
def form_parsing(html):
   tree = lxml.html.fromstring(html)
   data = {}
   for e in tree.cssselect('form input'):
      if e.get('name'):
         data[e.get('name')] = e.get('value')
   return data

def load_captcha(html): 
   tree = lxml.html.fromstring(html) 
   img_data = tree.cssselect('div#recaptcha img')[0].get('src') 
   img_data = img_data.partition(',')[-1] 
   binary_img_data = img_data.decode('base64') 
   file_like = BytesIO(binary_img_data) 
   img = Image.open(file_like) 
   return img 


#select (visa application type)
driver = webdriver.Chrome()
driver.get("https://ceac.state.gov/CEACStatTracker/Status.aspx")
 
# non immigrant visa type
select = Select(driver.find_element_by_name('ctl00$ContentPlaceHolder1$Visa_Application_Type'))
select.select_by_index(1)
# select Taiwan
selectLocation = Select(driver.find_element_by_name('ctl00$ContentPlaceHolder1$Location_Dropdown'))
selectLocation.select.select_by_value("TAI")
#input (immigrant visa case number)
searchterm = "2021162 635 0001"
sbox = driver.find_element_by_class_name("search-term")
sbox.send_keys(searchterm)
#LBD_CaptchaImage (enter code)
#
response = requests.get("https://ceac.state.gov/CEACStatTracker/Status.aspx")
soup = BeautifulSoup(response.text, "html.parser")
print(soup.prettify())
img = get_captcha(soup) 
img.save('captcha_original.png') 
gray = img.convert('L') 
gray.save('captcha_gray.png') 
bw = gray.point(lambda x: 0 if x < 1 else 255, '1') 
bw.save('captcha_thresholded.png') 
answer=pytesseract.image_to_string(bw) 
sbox = driver.find_element_by_id("Captcha")
sbox.send_keys(answer)
#click submit
submit = driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnSubmit")
submit.click()
#after click just get the result page
result = driver.find_element_by_id("ctl00_ContentPlaceHolder1_ucApplicationStatusView_lblMessage")
print(result)

