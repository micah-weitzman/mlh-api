#!flask/bin/python
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests, time

app = Flask(__name__)

def request_stuff(season, events):
    mlh_url = "https://mlh.io/seasons/%s/events" % (season)
    mlh_html = requests.get(mlh_url)
    soup = BeautifulSoup(mlh_html.content)
    event_list = soup.find_all('div', {'class':'col-lg-3'})
    for event_for in event_list:
        event_id = str(event_for)
        event_id = event_id[(event_id.find("event")+12):(event_id.find("event")+15)]
        if event_id in events:
            pass
        else:
            link_tag = str(event_for.find_all('a'))
            index = link_tag.find('"') + 1
            link = link_tag[index:]
            index = link.find('"')
            link = link[:index]

            event_head = str(event_for.find_all('h3'))
            index = event_head.find(">") + 1
            event_head = event_head[index:]
            index = event_head.find("<")
            event_head = event_head[:index]

            event_date = str(event_for.find_all('p'))
            index = event_date.find(">") + 1
            event_date = event_date[index:]
            index = event_date.find("<")
            event_date = event_date[:index]

            event_loc = str(event_for.find_all('p')[1])
            index = event_loc.find(">") + 1
            event_loc = event_loc[index:]
            index = event_loc.find("<")
            event_loc = event_loc[:index]

            event = {}
            event["location"] = event_loc
            event["date"] = event_date
            event["name"] = event_head
            event["link"] = link
            event["id"] = event_id
            events[event_id] = event
    



@app.route('/<string:mlh_season>')
def select_season(mlh_season):
    events_all = {}
    while True:
        request_stuff(mlh_season, events_all)
        return jsonify(events_all)
        # time to wait until refresh
        time.sleep(1800)

if __name__ == '__main__':
    app.run(debug=True)
