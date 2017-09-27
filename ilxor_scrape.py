import bs4
import urllib
import csv

def scrape_forum(url, board_id, thread_id):
    html = urllib.urlopen(url).read()
    # Make beautiful soup object
    soup = bs4.BeautifulSoup(html, "html.parser")

    title = soup.select('.headingblock h1')
    if (title and len(title) > 0):
        title = title[0].string

    message_containers = soup.select('div.message')
    post_num = 0

    for message_container in message_containers:
        user = next(iter(message_container.select('.posterinfo a') or []), None)
        # print(message_containers)

        body = message_container.find_all('p')

        if (body):
            body = body[0]
        if (body and user and body.string and user.string):
            post_num = post_num + 1
            with open('ilxor.csv', 'a') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([thread_id, board_id, post_num, user.string.encode('utf-8'), body.string.encode('utf-8')])
                

with open('ilxor.csv', 'wb') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['thread_id', 'thread_name', 'post_num', 'username', 'message'])

for i in range(10068, 20000):
    print('scraping thread', i)
    board_id = 41
    thread_id = i
    url = "https://www.ilxor.com/ILX/ThreadSelectedControllerServlet?action=showall&boardid={}&threadid={}#msg6187120".format(board_id, thread_id)

    scrape_forum(url, board_id, thread_id)
