
import requests
import codecs
from bs4 import BeautifulSoup as BS
from time import sleep


jobs = []
urls = []

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

base_url = 'https://djinni.co/jobs/?location=%D0%9A%D0%B8%D0%B5%D0%B2&primary_keyword=Python'
domain = 'https://djinni.co/'
urls.append(base_url)
urls.append(base_url + '&page=2')

for url in urls:
    sleep(2)
    request = session.get(url, headers=headers)
    if request.status_code == 200:
        bs = BS(request.content, 'html.parser')
        li_list = bs.find_all('li', attrs={'class': 'list-jobs__item'})

        for li in li_list:
            div = li.find('div', attrs={'class': 'list-jobs__title'})
            title = div.a.text
            href = div.a['href']
            intro = 'No description'
            desc = li.find('div', attrs={'class': 'list-jobs__description'})
            if desc:
                intro = desc.p.text

            jobs.append(
                {'href': domain + href,
                 'title': title,
                 'intro': intro,
                 # 'company': company
                 })
# data = bs.prettify()

template = '<!doctype html><html lang="en"><head><meta charset="utf-8"></head><body>'
content = '<h2> djinni.co</h2>'
end = '</body></html>'

for job in jobs:
    content += '<a href="{href}" target="_blank">{title}</a><br/><p>{intro}</p><br/>'.format(**job)
    content +=  '<hr/><br/><br/>'

data = template + content + end

handle = codecs.open('jobs.html', 'w', encoding='utf-8')
handle.write(str(data))
handle.close()