import requests
import xml.etree.ElementTree as ET
from datetime import datetime


def load_rss():
    url = "https://www.g4media.ro/feed"
    resp = requests.get(url)
    with open('topnewsfeed.xml', 'wb') as f:
        f.write(resp.content)
    return 'topnewsfeed.xml'


def parse_xml(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    news_items = []

    for item in root.findall('./channel/item'):
        news = {}
        for child in item:
            if child.tag == 'pubDate':
                original_date = child.text
                dt = datetime.strptime(original_date, "%a, %d %b %Y %H:%M:%S %z")
                formatted_date = dt.strftime("%d %b %Y %H:%M")
                news[child.tag] = formatted_date
            elif child.tag in ['title', 'link']:
                news[child.tag] = child.text
        news_items.append(news)
    news_items = sorted(news_items, key=lambda x: datetime.strptime(x['pubDate'], "%d %b %Y %H:%M"), reverse=True)
    return news_items


def get_today_news():
    xml_file = load_rss()
    news_items = parse_xml(xml_file)
    return news_items


def main():
    news_items = get_today_news()
    for item in news_items:
        print(item)


if __name__ == "__main__":
    main()
