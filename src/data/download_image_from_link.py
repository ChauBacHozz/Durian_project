import requests
import os
import json
import io
from PIL import Image

CURRENT_PATH = os.getcwd()
IMG_SAVE_PATH = "\\data\\raw\\images\\"
JSON_SAVE_PATH = "\\data\\raw\\images_link.json"

def download_image(download_path, url, file_name):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		if image.mode in ("RGBA", "P"): image = image.convert("RGB")
		file_path = download_path + file_name

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
	except Exception as e:
		print('FAILED -', e)

if os.path.exists(CURRENT_PATH + JSON_SAVE_PATH) and os.stat(CURRENT_PATH + JSON_SAVE_PATH).st_size == 0:
	link_dict = {}
	print("Json file blank")
else:
	
	with open(CURRENT_PATH + JSON_SAVE_PATH, encoding="utf-8-sig") as data_fp:
		link_dict = json.load(data_fp)
		print("Json file already have", len(link_dict), "links")
		for i in link_dict:
			print("Downloading",i)
			download_image(CURRENT_PATH + IMG_SAVE_PATH, link_dict[i], str(i) + ".jpg")
