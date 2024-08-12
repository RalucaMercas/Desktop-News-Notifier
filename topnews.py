import csv
import requests
import xml.etree.ElementTree as ET


def loadRSS():
    # url of rss feed
    url = "https://www.g4media.ro/feed"
    # creating HTTP response object from given url
    resp = requests.get(url)
    # saving the xml file
    with open('topnewsfeed.xml', 'wb') as f:
        f.write(resp.content)


def parseXML(xmlfile):
    # create element tree object
    tree = ET.parse(xmlfile)

    # get root element
    root = tree.getroot()

    # create empty list for news items
    newsitems = []

    # iterate news items
    for item in root.findall('./channel/item'):
        # empty news dictionary
        news = {}
        for child in item:
            if child.tag in ['title', 'link', 'description', 'pubDate']:
                news[child.tag] = child.text
        newsitems.append(news)
    return newsitems


def savetoCSV(newsitems, filename):
    # Specifying the fields for CSV file
    fields = ['title', 'link', 'description', 'pubDate']

    # Writing to CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(newsitems)


def printCSV(newsitems):
    for news in newsitems:
        print(news['title'])
        print(news['link'])
        print(news['description'])
        print(news['pubDate'])
        print("\n")


def main():
    loadRSS()
    newsitems = parseXML("topnewsfeed.xml")
    savetoCSV(newsitems, "topnews.csv")
    printCSV(newsitems)


if __name__ == "__main__":
    main()
