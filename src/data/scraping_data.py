from selenium import webdriver
import requests
import io
from PIL import Image
import os
import time
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
CURRENT_PATH = os.getcwd()
IMG_SAVE_PATH = "\\data\\raw\\"


def scroll_down(wd, delay):
	wd.execute_script("window.scrollTo(0, 800);")
	time.sleep(delay)

def get_images_from_google(wd, delay, max_images, keyword):
	print(max_images)
	url = f"https://www.google.com/search?sca_esv=b7c0b9c8093215b7&sca_upv=1&rlz=1C1FKPE_viVN1018VN1018&sxsrf=ACQVn09kl99i5HW4wEDTLOR4YE6I-VGy1w:1713575190392&q={keyword}&uds=AMwkrPuhn_F0WDJCwQwE6XxpOj7eCFqU10ejyinwiyfy6WD8Yp9ndcq7xiby0NsL55Iim-DgpC2yIn2igPl3oj43ebZ5hkPp9wn6GGYk1xBGzvRSQcHGPR-FhcemBr8QG3UQWNeHFaGjB5hXLKZZ247HLhWpZSOapQLfp0bgrCZlAfAtI_bYACKkXRR-fN0CmNntf6GVKMsw-REt1RXmMXl5eZx01--dLe_hWrPjDXNeSYQIrUZDDHhWUbQvTueKr0U5E71MRX21xZ6_fl1bd2di2kV69dZtZq0TqjqUDP7RvvZ269a1avMu-tDD093diXwHA4x7twQO&udm=2&prmd=isvnbtz&sa=X&ved=2ahUKEwiFtZOEzc-FAxWlyzgGHaFYBd8QtKgLegQIEBAB&biw=1372&bih=649&dpr=1.4"
	wd.get(url)
	image_urls = set()
	skips = 0
	time.sleep(delay)
	while len(image_urls) < max_images:
		scroll_down(wd, delay)
		thumbnails = wd.find_elements(By.CLASS_NAME, "H8Rx8c")
		for img in thumbnails[len(image_urls) + skips: max_images + skips + 1]:
			try:
				img.click()
				time.sleep(delay)
			except:
				continue
			images = wd.find_elements(By.XPATH, "//img[contains(@class, 'sFlh5c pT0Scc iPVvYb')]")
			for image in images:
				if image.get_attribute('src') in image_urls:
					skips += 1
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

urls = get_images_from_google(driver, 1, 20, keyword='durian')

for i, url in enumerate(urls):
	download_image(CURRENT_PATH + IMG_SAVE_PATH, url, str(i) + ".jpg")

driver.quit()