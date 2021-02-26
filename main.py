import requests, firebase_admin
from bs4 import BeautifulSoup
from datetime import datetime
from firebase_admin import credentials
from firebase_admin import db

final = {}
current_time = datetime.now().strftime('%H:%M:%S')
article_count = 1
error_count = 1


def GoToLink(page):
    articles = BeautifulSoup(page.text, "lxml").findAll('div', class_='news_Itm')
    global article_count
    global error_count

    for article in articles:
        try:
            aditya = current_time
            author = article.find('span', class_='posted-by').a.getText()
            description = article.find('p', class_='newsCont').getText()
            heading_1 = article.find('h2', class_='newsHdng').getText()
            heading_2 = article.find('p', class_='newsCont').getText()
            image = article.find('div', class_='news_Itm-img').img['src']
            link = article.find('h2', class_='newsHdng').a['href']

            if aditya is not None and description is not None and heading_1 is not None and heading_2 is not None and image is not None and link is not None:
                final[article_count] = {
                    'ADITYA': aditya,
                    'Author': author,
                    'Description': description,
                    'Heading1': heading_1,
                    'Heading2': heading_2,
                    'Image': image,
                    'Link': link
                }

        except AttributeError:
            error_count += 1

        article_count += 1


def GetNews():
    page_count = 1
    while True:
        page_url = 'http://www.ndtv.com/latest/page-' + str(page_count)
        page = requests.get(page_url)
        if page.status_code == 200:
            GoToLink(page)
            page_count += 1
        else:
            break


def SaveToFirebase():
    credential = credentials.Certificate('private.json')
    firebase_admin.initialize_app(credential, {
        'databaseURL': 'https://inshorts-raja-default-rtdb.firebaseio.com/'
    })
    db.reference().child('News').set(final)
    print("Article Count = " + str(article_count) + " Error Count = " + str(error_count) + " Precision Rate = " + str(100 - (error_count/article_count)) + "%")
    print("Last Updated @ " + current_time)


GetNews()
SaveToFirebase()
