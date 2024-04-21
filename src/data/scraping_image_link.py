import json
from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from icecream import ic
class Durian_IMGlink():
    def __init__(self, link):
        self.status = "Not downloaded"
        self.link = link
        self.id = None
		
def scroll_down(wd, delay):
	wd.execute_script("window.scrollTo(0, 800);")
	time.sleep(delay)

def get_images_from_google(wd, delay, max_images, keyword, link_dict):
	print("Number query images:", max_images)
	url = f"https://www.google.com/search?sca_esv=b7c0b9c8093215b7&sca_upv=1&rlz=1C1FKPE_viVN1018VN1018&sxsrf=ACQVn09kl99i5HW4wEDTLOR4YE6I-VGy1w:1713575190392&q={keyword}&uds=AMwkrPuhn_F0WDJCwQwE6XxpOj7eCFqU10ejyinwiyfy6WD8Yp9ndcq7xiby0NsL55Iim-DgpC2yIn2igPl3oj43ebZ5hkPp9wn6GGYk1xBGzvRSQcHGPR-FhcemBr8QG3UQWNeHFaGjB5hXLKZZ247HLhWpZSOapQLfp0bgrCZlAfAtI_bYACKkXRR-fN0CmNntf6GVKMsw-REt1RXmMXl5eZx01--dLe_hWrPjDXNeSYQIrUZDDHhWUbQvTueKr0U5E71MRX21xZ6_fl1bd2di2kV69dZtZq0TqjqUDP7RvvZ269a1avMu-tDD093diXwHA4x7twQO&udm=2&prmd=isvnbtz&sa=X&ved=2ahUKEwiFtZOEzc-FAxWlyzgGHaFYBd8QtKgLegQIEBAB&biw=1372&bih=649&dpr=1.4"
	wd.get(url)
	image_urls = set()
	skips = 0
	time.sleep(delay)
	while len(image_urls) < max_images:
		scroll_down(wd, delay)
		thumbnails = wd.find_elements(By.CLASS_NAME, "H8Rx8c")
		for img in thumbnails[len(image_urls) + skips: max_images + skips]:
			try:
				img.click()
				time.sleep(delay)
			except:
				continue
			images = wd.find_elements(By.XPATH, "//img[contains(@class, 'sFlh5c pT0Scc iPVvYb')]")
			for image in images:
				link = image.get_attribute('src')
				if (link in image_urls) or (link in link_dict.values()):
					skips += 1
					break
				if link and 'http' in link:
					image_urls.add(link)
					link_dict[f"{len(link_dict)}"] = link
					print(f"Found {len(image_urls)}")
	return link_dict

		
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
CURRENT_PATH = os.getcwd()
JSON_SAVE_PATH = "\\data\\raw\\images_link.json"

if os.path.exists(CURRENT_PATH + JSON_SAVE_PATH) and os.stat(CURRENT_PATH + JSON_SAVE_PATH).st_size == 0:
	link_dict = {}
else:
	with open(CURRENT_PATH + JSON_SAVE_PATH, encoding="utf-8-sig") as data_fp:
		link_dict = json.load(data_fp)
print(type(link_dict))
res = get_images_from_google(wd=driver, delay=1, max_images=10, 
							 keyword='durian', link_dict=link_dict)
with open(CURRENT_PATH + JSON_SAVE_PATH, 'w') as data_fp:
    json.dump(res, data_fp, indent=4)
# with open(CURRENT_PATH + JSON_SAVE_PATH, encoding="utf-8-sig") as data_fp:
#     res = json.load(data_fp)
# print(type(res[0]))
driver.quit()
