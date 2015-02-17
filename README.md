#Unofficial Major League Hacking API

Welcome to the Unoffical MLH API. This is not the offical API used by MLH, but simply one I made at CodeDay Winter 2015.
The API is a simple REST made in Flask that utilizes BeautifulSoup. It scrapes information off of [mlh.io](http://mlh.io) and returns it in a neat JSON format. 

The index returns all the events for the current seasons, both in Europe and the US. Appending `s2015` for the current US season, and `eu-2015` for the European, provides all the information for its location respectively. 

The app returns basic information about each event including the offical id, data, link, location, and name.  
The mapping for an event is `event/name_of_event/`. In the following example the information is pulled from `event/dragon%20hacks/`.

``` json
"Dragon Hacks": {
    "date": "January 10th - 11th",
    "id": "102",
    "link": "http://www.hack-dragon.com",
    "location": "Philadelphia, PA",
    "name": "Dragon Hacks"
  },
  ```
  You can also select individual querys of hackathons such as the `link` or `id` using the url mapping `/search/name_of_hackathon/value/`. For example `search/dragon%20hacks/date/` would return  
  ``` text
  January 10th - 11th
 ```
 
 or `search/dragon%20hacks/link/` would return  
 ``` text
 http://www.hack-dragon.com
 ```
  
  
  Feel free to edit and manipulate the code as you like. I hope this code is as useful as I thought it would be. 
