import requests
from lxml import etree
import sys

# Read irna news
print('Crawling irna news https://www.irna.ir/news/xxx')

#First URL
#URL = "https://www.irna.ir/news/4001740/"

#Last URL
#URL = "https://www.irna.ir/news/84861397/"

news_counter = 4001740
try:
    last_id_f = open('last-news-id.txt', 'r', encoding="utf-8")
    news_counter = int(last_id_f.readline().strip())
    last_id_f.close()
except:
    print(f'Crawling from scratch! news id = {news_counter}')
    
with open('irna.txt', 'a', encoding="utf-8") as f:
    while news_counter <= 84861397:
        print(f'news id = {news_counter}')
        try:
            last_id_f = open('last-news-id.txt', 'w', encoding="utf-8")
            last_id_f.write(str(news_counter).strip())
            last_id_f.close()
        except:
            print('IO Error!')
            
        URL = f"https://www.irna.ir/news/{news_counter}/"
        news_counter = news_counter + 1
        try:
            resp = requests.get(URL)
            if resp.status_code == 200:
                dom = etree.HTML(resp.text)

                # Print news title
                title = dom.xpath("//div[@class='item-title']/h1[@class='title']")
                if title!=[]:
                    f.write(etree.tostring(title[0], method="text", encoding="unicode").strip())

                # Print news sumary
                sumary = dom.xpath("//div[@class='item-summary']/p[@class='summary introtext']")
                if sumary!=[]:
                    f.write(etree.tostring(sumary[0], method="text", encoding="unicode").strip())

                # Print news text
                news_text = dom.xpath("//div[@class='item-text']/p")
                if news_text==[]: # old page
                    news_text = dom.xpath("//div[@class='item-text old']")

                if news_text!=[]:       
                    for text in news_text:
                        f.write(etree.tostring(text, method="text", encoding="unicode").strip())
        except:
            print('Read data Error!')
