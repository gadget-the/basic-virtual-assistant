import bs4 as bs
import requests, urllib, time#, xml#, nltk
# from nltk import ne_chunk, pos_tag, word_tokenize
# from nltk.tree import Tree
import geocoder
from geopy.geocoders import Nominatim

app = Nominatim(user_agent="tutorial")

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

# def get_continuous_chunks_1(text):
#   chunked = ne_chunk(pos_tag(word_tokenize(text)))
#   #prev = None
#   continuous_chunk = []
#   current_chunk = []
  
#   for subtree in chunked:
#     if type(subtree) == Tree and subtree.label() == 'GPE':
#       current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
#     elif current_chunk:
#       named_entity = " ".join(current_chunk)
#       if named_entity not in continuous_chunk:
#         continuous_chunk.append(named_entity)
#         current_chunk = []
#     else:
#       continue

#   return continuous_chunk

def weatherGrab(location):
  #print(type(location))
  main_url = "https://www.google.com/search?q=weather+"
  reqUrl = ""
  if type(location) == list:
    reqUrl = main_url + "+".join(location).replace(" ", "+").replace(",", "+").lower()
    # print("weather for", ", ".join(location))
  elif type(location) == str:
    reqUrl = main_url + location.replace(" ", "+").replace(",", "+").lower()
    # print("weather for", location)
  #print(reqUrl)
  try:
    soup = bs.BeautifulSoup(requests.get(reqUrl).content, 'html.parser')
  except Exception as e:
    return ("Unable to get weather, due to: " + str(e) + " Error")
  #print(soup)
  #print(soup.prettify())
  
  temp = soup.find("div", attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
  tns = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
  tns = tns.split('\n')
  time = tns[0]
  sky = tns[1]
  # listdiv = list(set([s.text for s in soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})]))

  # hum = None
  # wnd = None
  # for i in listdiv:
  #   if "Wind" in i:
  #     wnd_holder = i
  #     break

  # wnd = wnd_holder[wnd_holder.find('W'):]
  # print(wnd, hum)
  # print(tns, wnd, hum, reqUrl)
  # print(listdiv, tns, reqUrl)

  return temp, sky#, time, listdiv

# def takeInput(inSent = ""):
#   #we assume that we've already verified that a request was made for the weather
#   #inSent = "What's the weather like in Paris?"
#   if not inSent:
#     inSent = input('> ')
#   # print(inSent[-1])
#   if inSent[-1] not in ["?", ".", ",", ";"]:
#     inSent += "?"
#   # print(inSent)
#   gpeExtrac = get_continuous_chunks_1(inSent)
#   if gpeExtrac:
#     # gpeExtrac = [bit[0].upper() + bit[1:] for bit in gpeExtrac]
#     #print(gpeExtrac)
#     return weatherGrab(gpeExtrac)
#   else:
#     weatherLoc = input("weather where?(capitalize)\n>")
#     return weatherGrab(weatherLoc)

def get_address_by_location(latitude, longitude, language="en"):
    """This function returns an address as raw from a location
    will repeat until success"""
    # build coordinates string to pass to reverse() function
    coordinates = f"{latitude}, {longitude}"
    # sleep for a second to respect Usage Policy
    time.sleep(1)
    try:
        return app.reverse(coordinates, language=language).raw
    except:
        return get_address_by_location(latitude, longitude)

def get_current_location():
  g = geocoder.ip('me')
  # print(g.latlng)
  addr = get_address_by_location(g.latlng[0], g.latlng[1])
  # print([addr['address']['city'], addr['address']['state'], addr['address']['country']])
  city = addr['address']['city'] if addr['address']['city'] else None
  state = addr['address']['state'] if addr['address']['state'] else None
  country = addr['address']['country'] if addr['address']['country'] else None
  return [city, state, country]

def get_latlong(loc):
  if type(loc) == list:
    loc = ", ".join(loc)
  
  url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(loc) +'?format=json'
  response = requests.get(url).json()

  return response[0]["lat"], response[0]["lon"]

def get_weather_data(location = None, latlng = None, tmp = False, sk = False, wnd = False, humi = False, detFor = False):
  main_url = "https://forecast.weather.gov/MapClick.php?"
  reqUrl = "" # https://forecast.weather.gov/MapClick.php?lat=33.74831000000006&lon=-84.39110999999997 - xml?: https://forecast.weather.gov/MapClick.php?lat=37.3974&lon=-122.0831&unit=0&lg=english&FcstType=dwml

  if not location:#if no location is specified, grab the current location of the user and use that
    latlng = geocoder.ip('me').latlng
    location = ", ".join(get_current_location())
  else:
    latlng = get_latlong(location)#get the latitude and longitude of the location

  reqUrl = main_url + "lat=" + str(latlng[0]) + "&lon=" + str(latlng[1])# piece together the url to make the request
  # print(reqUrl)

  try:
    soup = bs.BeautifulSoup(requests.get(reqUrl).content, 'html.parser')
  except Exception as e:
    return ("Unable to get weather, due to: " + str(e) + " Error")

  # temp = soup.find("p", attrs={'class': 'myforecast-current-lrg'}).text
  # tempC = soup.find("p", attrs={'class': 'myforecast-current-sm'}).text

  # tble = soup.find_all("tr")
  # wind = tble[1].find_all("td")[1].text
  # hum = tble[0].find_all("td")[1].text
  # upd = tble[-1].find_all("td")[1].text.replace("  ", "").replace("\n", "")
  # detForecast = [i.text for i in soup.find("div", attrs={'id': 'detailed-forecast-body'}).find_all("div",  attrs={'class': 'col-sm-10 forecast-text'})]

  try:
    temp = soup.find("p", attrs={'class': 'myforecast-current-lrg'}).text# temp in farenheit
    tempC = soup.find("p", attrs={'class': 'myforecast-current-sm'}).text# temp in celcius

    tble = soup.find_all("tr")
    wind = tble[1].find_all("td")[1].text# wind direction and speed
    hum = tble[0].find_all("td")[1].text# humidity
    upd = tble[-1].find_all("td")[1].text.replace("  ", "").replace("\n", "")# get the time at which the information on the page was last updated
    # extFore = [i.text for i in soup.find("div", attrs={'id': 'seven-day-forecast'}).find_all("p", attrs={'class': 'short-desc'})]
    extFore = [str(i).replace("<br/>", " ").replace('<p class="short-desc">', "").replace("</p>", " ") for i in soup.find("div", attrs={'id': 'seven-day-forecast'}).find_all("p", attrs={'class': 'short-desc'})]# extended forecast information
    sky = extFore[0]
    detForecast = [i.text for i in soup.find("div", attrs={'id': 'detailed-forecast-body'}).find_all("div",  attrs={'class': 'col-sm-10 forecast-text'})]
    #["Today", "Tonight", "Saturday", "Saturday Night", "Sunday", "Sunday Night", "Monday", "Monday Night", "Tuesday", "Tuesday Night", "Wednesday", "Wednesday Night", "Thursday"]
    #essentially today and tonight, tomorrow and tomorrow night, and so on for 7 days and nights minus the last night
  except Exception as e:# if the previous attempt fails, just use the old weatherGrab function
    # print(e)
    w = weatherGrab(location)
    temp = w[0]
    sky = w[1]
    wind = None
    hum = None
    upd = None
    detForecast = None
    # try:
    #   w = weatherGrab(location)
    #   temp = w[0]
    #   sky = w[1]
    #   wind = None
    #   hum = None
    #   upd = None
    #   detForecast = None
    # except Exception as e:# if that doesn't work
    #   return "Could not get weather data for " + location + " due to '" + str(e) + "' Error"
    # return "Could not get weather data for " + location + " due to '" + str(e) + "' Error"

  # print(temp)
  # print(tempC)
  # print(wind)
  # print(hum)
  # print(upd)
  # print(sky)
  # print(extFore)
  # print(detForecast)
  out = []
  
  if tmp:# add the requested information to the ouput
    out.append(temp)

  if sk:
    out.append(sky)
  
  if wnd:
    out.append(wind)

  if humi:
    out.append(hum)

  if detFor:
    out.append(detForecast[0])
  
  out.extend([location, upd])# add the location and last update time to the output
  # out.append(upd)

  # return temp, wind, hum, upd#, reqUrl
  return tuple(out)# output a tuple

if __name__ == "__main__":
  # takeInput("Los Angeles")
  # print(get_continuous_chunks_1(input('> ')))
  # weatherGrab("los angeles")

  # print(get_address_by_location(32.89068, 90.67516))

  # print(get_current_location())
  # print(weatherGrab(get_current_location()))

  # print(get_latlong("Dubai, Dubayy, United Arab Emirates"))
  # print(get_latlong("Mountain View, CA"))

  # "AttributeError: 'NoneType' object has no attribute 'text'" - line 167, in get_weather_data - https://forecast.weather.gov/MapClick.php?lat=25.2653471&lon=55.2924914 - it's because weather.gov only has data for the united states
  print(get_weather_data("Dubai, United Arab Emirates"))
  # "IndexError: list index out of range" - line 173, in get_weather_data - https://forecast.weather.gov/MapClick.php?lat=37.3893889&lon=-122.0832101 - FIXED
  print(get_weather_data("Mountain View, CA"))
  print(get_weather_data("Atlanta, Georgia"))
  print(get_weather_data("Los Angeles"))
  print(get_weather_data(location="Los Angeles", tmp=True))
  print(get_weather_data())
  # print(get_weather_data(detFor=True))

'''
https://replit.com/@TheRicks2/Named-Entity-Recognition-Test-2#main.py
stuff from stackoverflow #2 - https://stackoverflow.com/questions/48660547/how-can-i-extract-gpelocation-using-nltk-ne-chunk
https://www.geeksforgeeks.org/how-to-extract-weather-data-from-google-in-python/
https://stackoverflow.com/questions/25888396/how-to-get-latitude-longitude-with-python

https://openweathermap.org/current
https://github.com/csparpa/pyowm
weather.gov
'''