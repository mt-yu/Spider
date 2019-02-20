import requests
from bs4 import BeautifulSoup
import os
url = 'https://cn.bing.com/'
kv = {'user-agent':'Mozilla//5.0'}
try:
	r = requests.get(url, stream=True, headers=kv)
	soup = BeautifulSoup(r.text, 'html.parser')
	# 获取对应的图片连接 img_url
	src = soup.head.link['href']
	img_url = url + src
	# 设置图片名称
	name = src.split('/')[-1]

	r_img = requests.get(img_url, stream=True)
	with open('F:/mt/6 project/9 material/BingImage/' + name, 'wb') as f:
		for chunk in r_img.iter_content(chunk_size=128):
			f.write(chunk)
except Exception as e:
	print(e)
	os.system('pause')





