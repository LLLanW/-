import requests
from lxml import etree

requests.header = {'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
response = requests.get('http://piyao.sina.cn/')
html = etree.HTML(response.content)

text = html.xpath('//li/a//div[left_title]')
good_str = html.xpath('//li/a//div[like_text]')

good_and_text = zip(good_str,text)
good_and_text = (list)good_and_text
good = sorted(good_and_text,lambda x:x[0])

print("新浪十大谣言：")
for x in good[:10]:
    print("点赞数：",x[0],'\t',x[1])
