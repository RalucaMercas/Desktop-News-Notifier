import requests
import xml.etree.ElementTree as ET
from datetime import datetime


def loadRSS():
    url = "https://www.g4media.ro/feed"
    resp = requests.get(url)
    with open('topnewsfeed.xml', 'wb') as f:
        f.write(resp.content)
    return 'topnewsfeed.xml'


def parseXML(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    newsitems = []

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
        newsitems.append(news)
    return newsitems


def topStories():
    xmlfile = loadRSS()
    newsitems = parseXML(xmlfile)
    return newsitems


def main():
    newsitems = topStories()
    for item in newsitems:
        print(item)


if __name__ == "__main__":
    main()
