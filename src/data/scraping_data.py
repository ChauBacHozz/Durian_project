from selenium import webdriver
import requests
import io
from PIL import Image
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

service_obj = Service("F:\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
# options.add_argument('--headless')
driver = webdriver.Chrome(service=service_obj, options=options)
current_wd = os.getcwd()
img_saving_path = "\\data\\external\\"
# image_url = "https://www.producereport.com/sites/default/files/styles/large/public/field/image/durians_9.jpg?itok=7f-jOKwp"
# def scroll_down(wd):
#     wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(1)

def get_images_from_google(wd, delay, max_images):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)

	url = "https://www.google.com/search?sca_esv=b7c0b9c8093215b7&sca_upv=1&rlz=1C1FKPE_viVN1018VN1018&sxsrf=ACQVn09kl99i5HW4wEDTLOR4YE6I-VGy1w:1713575190392&q=durian&uds=AMwkrPuhn_F0WDJCwQwE6XxpOj7eCFqU10ejyinwiyfy6WD8Yp9ndcq7xiby0NsL55Iim-DgpC2yIn2igPl3oj43ebZ5hkPp9wn6GGYk1xBGzvRSQcHGPR-FhcemBr8QG3UQWNeHFaGjB5hXLKZZ247HLhWpZSOapQLfp0bgrCZlAfAtI_bYACKkXRR-fN0CmNntf6GVKMsw-REt1RXmMXl5eZx01--dLe_hWrPjDXNeSYQIrUZDDHhWUbQvTueKr0U5E71MRX21xZ6_fl1bd2di2kV69dZtZq0TqjqUDP7RvvZ269a1avMu-tDD093diXwHA4x7twQO&udm=2&prmd=isvnbtz&sa=X&ved=2ahUKEwiFtZOEzc-FAxWlyzgGHaFYBd8QtKgLegQIEBAB&biw=1372&bih=649&dpr=1.4"
	wd.get(url)
	image_urls = set()
	skips = 0
	time.sleep(2)
	while len(image_urls) < max_images:
		scroll_down(wd)
		thumbnails = wd.find_elements(By.CLASS_NAME, "H8Rx8c")
		for img in thumbnails[len(image_urls) + skips:max_images]:
			try:
				img.click()
				time.sleep(2)
			except:
				continue
			# time.sleep(2)
			images = wd.find_elements(By.XPATH, "//img[contains(@class, 'sFlh5c pT0Scc iPVvYb')]")
			for image in images:
				if image.get_attribute('src') in image_urls:
				# 	max_images += 1
				# 	skips += 1
					break

				if image.get_attribute('src') and 'http' in image.get_attribute('src'):
					image_urls.add(image.get_attribute('src'))
					print(f"Found {len(image_urls)}")
	return image_urls

def download_image(download_path, url, file_name):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path + file_name

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
	except Exception as e:
		print('FAILED -', e)

urls = get_images_from_google(driver, 1, 5)

for i, url in enumerate(urls):
	download_image(current_wd + img_saving_path, url, str(i) + ".jpg")

# driver.quit()