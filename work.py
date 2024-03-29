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

base_url = 'https://www.work.ua/jobs-kyiv-python/?setlp=ru'
domain = 'https://www.work.ua/'
urls.append(base_url)

request = session.get(base_url, headers=headers)

if request.status_code == 200:
    bs = BS(request.content, 'html.parser')
    pagination = bs.find('ul', attrs={'class': 'pagination'})

    if pagination:
        pages = pagination.find_all('li', attrs={'class': False})
        for page in pages:
            urls.append(domain + page.a['href'])

for url in urls:
    sleep(2)
    request = session.get(url, headers=headers)
    if request.status_code == 200:
        bs = BS(request.content, 'html.parser')
        div_list = bs.find_all('div', attrs={'class': 'job-link'})

        for div in div_list:
            title = div.find('h2')
            href = domain + title.a['href']
            intro = div.p.text
            company = 'No name'
            logo = div.find('img')

            if logo:
                company = logo['alt']

            jobs.append(
                {'href': domain + href,
                 'title': title.text,
                 'intro': intro,
                 'company': company})
# data = bs.prettify()

template = '<!doctype html><html lang="en"><head><meta charset="utf-8"></head><body>'
content = '<h2> Work.ua</h2>'
end = '</body></html>'

for job in jobs:
    content += '<a href="{href}" target="_blank">{title}</a><br/><p>{intro}</p><p>{company}</p><br/>'.format(**job)
    content +=  '<hr/><br/><br/>'

data = template + content + end

handle = codecs.open('jobs.html', 'w', encoding='utf-8')
handle.write(str(data))
handle.close()
