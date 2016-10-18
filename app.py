#!flask/bin/python
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests, time
import urllib
import datetime

app = Flask(__name__)
year = str(datetime.date.today().year)

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
            index = link_tag.find('"') +  1
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

            #This is for getting the city
            event_loc = str(event_for.find_all('span'))
            index = event_loc.find(">") + 1
            event_loc = event_loc[index:]
            index = event_loc.find("<")
            event_loc_city = event_loc[:index]
            
            #This is for getting the state, I added +9 because after it was ending -
            #- at "</span>, ". +9 just moves the pointer forward.            
            event_loc = event_loc[index+9:]
            index = event_loc.find(">") + 1
            event_loc = event_loc[index:]
            index = event_loc.find("<")
            event_loc_state = event_loc[:index]
            event_loc = event_loc_city+ ", " + event_loc_state

            event = {}
            event["location"] = event_loc
            event["date"] = event_date
            event["name"] = event_head
            event["link"] = link
            event["id"] = event_id
            events[event_head] = event
    

@app.route('/')
def index():
    us_event = {}
    request_stuff("s" + year, us_event)
    eu_event = {}
    request_stuff("s"+year+"-eu", eu_event)
    event_all = {"us_event":us_event,"eu_event":eu_event}
    return jsonify(event_all)


@app.route('/<string:mlh_season>/')
def select_season(mlh_season):
    events_all = {}
    while True:
        request_stuff(mlh_season, events_all)
        return jsonify(events_all)
        # time to wait until refresh
        time.sleep(1800)

@app.route('/event/<string:mlh_event>/')
def search_event(mlh_event):
    us_event = {}
    request_stuff("s"+year, us_event)
    eu_event = {}
    request_stuff("s"+year+"-eu", eu_event)
    for evnt in us_event:
        if urllib.unquote(mlh_event.lower()) == evnt.lower():
            return jsonify(us_event[evnt])
        else:
            for i in eu_event:
                if urllib.unquote(mlh_event.lower()) == i.lower():
                    return jsonify(eu_event[i])

@app.route('/search/<string:mlh_event>/<string:key_>/')

def search_by_key(mlh_event, key_):
    us_event = {}
    request_stuff("s"+year, us_event)
    eu_event = {}
    request_stuff("s"+year+"-eu", eu_event)
    for evnt in us_event:
        if urllib.unquote(mlh_event.lower()) == evnt.lower():
            return us_event[evnt][key_]
        else:
            for i in eu_event:
                if urllib.unquote(mlh_event.lower()) == i.lower():
                    return eu_event[i][key_]


if __name__ == '__main__':
    app.run(debug=True, port=50981
    )
