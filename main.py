import json
import requests
import matplotlib.pyplot as plt
from plotly.graph_objs import Scattergeo, Layout
from datetime import datetime
from plotly import offline
from plotly.graph_objs import Bar, Layout
import pygal
import numpy as np
import pandas as pd
from operator import sub
import plotly.graph_objects as go

cities_list = ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa', 'Winnipeg', 'Quebec City',
'Hamilton', 'Kitchener', 'London', 'Victoria', 'Halifax', 'Oshawa', 'Windsor', 'Saskatoon', 'St. Catharines', 'Regina', 'St. Johns', 'Kelowna']

filename = 'data.json'
"""
url = 'https://api.openweathermap.org/data/2.5/weather?q=Toronto,CA&appid=69b4b10c268681bc7477590962f3b6dd'
filename = 'data.json'

city1 = []

for city_name in cities_list:
  url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name},CA&appid=69b4b10c268681bc7477590962f3b6dd"
  r = requests.get(url)
  print(city_name)
  print(f"Status code: {r.status_code}")
  response_dict =r.json()
  print(response_dict.keys())
  city1.append(response_dict)

#using filename to  dump data
##use 'a' first the change to 'w'
with open(filename, 'w') as file_object:
    json.dump(city1, file_object, indent = 4)"""

with open(filename) as file_object:
  all_eq_data = json.load(file_object)

###creating empty lists and for loop
temperatures, long, lats = [], [], []
for eq_dict in all_eq_data:
  temp = eq_dict['main']['temp'] 
  lon = eq_dict['coord']['lon']
  lat = eq_dict['coord']['lat']
  temperatures.append(temp)
  long.append(lon)
  lats.append(lat)


print(temperatures)
###creating plot
my_layout = Layout(title = 'Cities Temperature')

data = [{
  'type':'scattergeo',
  'lon':long,
  'lat':lats,
  "marker": {
    "size":[0.3*mag for mag in temperatures],
    "color":temperatures,
    "colorscale":"Viridis",
    "reversescale":True,
    "colorbar": {"title": "Magnitude"},
  },
}]

figure = {'data': data, 'layout': my_layout}
offline.plot(figure, filename = '1map.html')

######Q1b
##creating empty lists
humidities, long, lats = [], [], []
##creating for loops
for eq_dict in all_eq_data:
  humid = eq_dict['main']['humidity'] 
  lon = eq_dict['coord']['lon']
  lat = eq_dict['coord']['lat']
  humidities.append(humid)
  long.append(lon)
  lats.append(lat)


print(humidities)
##creating plot with scattergeo
my_layout = Layout(title = 'Cities Humidity')

data = [{
  'type':'scattergeo',
  'lon':long,
  'lat':lats,
  "marker": {
    "size":[0.3*mag for mag in humidities],
    "color":humidities,
    "colorscale":"Viridis",
    "reversescale":True,
    "colorbar": {"title": "Humidities (g/m3)"},
  },
}]

figure = {'data': data, 'layout': my_layout}
offline.plot(figure, filename = '2map.html')

#########
#######1c
#########
##creating cities variable
x_values = cities_list
##creating empty list
labels, temps, hums = [], [], []
##creating for loop
for data in all_eq_data:
  name = data['name']
  labels.append(name)
  humi = data['main']['humidity']
  hums.append(humi)
  temper = data['main']['temp']
  temps.append(temper)

##setting y-values
y_values1 = temps
y_values2 = hums

x = np.arange(len(labels))
w = 0.25
fig, ax1 = plt.subplots(figsize = (15, 9))
##creatings bars
ax2 = ax1.twinx()
ax1.bar( x - w/2, y_values1, w, color = 'red', label = 'temperatures', align = 'edge')
ax2.bar(x + w/2, y_values2, w, color = 'yellow', label = 'humidities', align = 'edge')

plt.title('Temperature and Humidity Chart')
plt.xticks(x, labels)
for tick in ax1.get_xticklabels():
  tick.set_rotation(50)
##setting labels and legend
ax1.set_ylabel('Temperature(kelvin)')
ax2.set_ylabel('Humidity')
ax1.set_xlabel('cities_list')
ax1.legend(['Temperatue'], loc = 'upper left')
ax2.legend(['Humidity'], loc = 'upper right')

plt.savefig('clusterbar.png', bbox_inches = 'tight')


########
######2
########
##creating empty list
description_data = []
##creating for loop to append data
for data in all_eq_data:
  climate = data["weather"][0]["description"]
  description_data.append(climate)

unique_count = {}

for numb in description_data:
  if numb in unique_count:
    unique_count[numb] +=1
  else:
    unique_count[numb] = 1

print (unique_count)

x_valuesbar = list(unique_count.keys())
y_valuesbar = list(unique_count.values())

data = [Bar(x = x_valuesbar, y = y_valuesbar)]

x_axis_config = {'title' : 'Unique Weather Description'}
y_axis_config = {'title' : 'Count'}

my_layout = Layout(title = 'Count of Unique Weather Description', xaxis = x_axis_config, yaxis = y_axis_config)

offline.plot({'data': data, 'layout': my_layout}, filename = 'uniquedescription.html')

#####
#####3
##creating empty lists
speeds, cities = [], []
##creating for loop and appending city and speed data
for data in all_eq_data:
  speed = data['wind']['speed']
  name = data['name']
  speeds.append(speed)
  cities.append(name)


highest = max(speeds) 
lowest = min(speeds)
##extracting max and minimum speeds
cityspeed = {}
counter = 0
for city in cities:
  cityspeed[city] = speeds[counter]
  counter += 1
##printing city speeds
for key, value in cityspeed.items():
  if value == highest:
    print(f'The city with the maximum wind speed, with a wind speed of {value} is {key}')
  elif value == lowest:
    print(f'The city with the minimum wind speed, with a wind speed of {value} is {key}')


#####
#####4
######
##creating empty list for sunrise and sunset values
sunrisevalue, sunsetvalue = [], []
##extracting and appending data
for data in all_eq_data:
  sunset = data['sys']['sunset']
  sunrise = data['sys']['sunrise']
  sunsetvalue.append(sunset)
  sunrisevalue.append(sunrise)

###subtracting difference and storing in varible
difference = []
sunlight = zip(sunsetvalue, sunrisevalue)
for daylight1, daylight2 in sunlight:
  difference.append(daylight1 - daylight2)

###converting into string of datetime format
sundurations = []
for value in difference:
  timestamp = datetime.utcfromtimestamp(value).strftime('%H:%M')
  sundurations.append(timestamp)
  print(sundurations)
##
sun = {}
counter = 0
for city in cities_list:
  sun[city] = sundurations[counter]
  counter +=1
##printing duration statement
for key, value in sun.items():
  print(f"Sunlight duration in {key}, was {value[:2]}hours and {value[3:]}mins")

##feeding sundurations as argument
def avgtime(timestringlist):
  minutecounts = []
  for val in timestringlist:
    h = val[:2]
    m = val[3:5]
    total_minutes = (int(h)*60) + int(m)
    minutecounts.append(total_minutes)
  avgtimemins = sum(minutecounts)/len(minutecounts)
  hours = int(avgtimemins/60)
  minutes = avgtimemins % 60
  return f"{hours} hours and {minutes} minutes"
print(f"The average duration of light today for all cities is {avgtime(sundurations)}")

#######
######5
#######
###extracting data
temperature, feelliketemp, city_name = [], [], []

for data in all_eq_data:
  temp = data['main']['temp']
  feels_like = data['main']['feels_like']
  cities_name = data['name']
  temperature.append(temp)
  feelliketemp.append(feels_like)
  city_name.append(cities_name)
###calculating difference
tempdiff = []
diff = zip(temperature, feelliketemp)
for diff1, diff2 in diff:
  tempdiff.append(diff1 - diff2)

print(tempdiff)
###printing difference statement
for city, diff in zip(city_name, tempdiff):
  print(f"the difference in the actual temperature and feels for {city}, is {diff} degrees")



#####
####6
#####
##creating empty list
speeds, cities = [], []
##extracting citing
for data in all_eq_data:
  speed = data['wind']['speed']
  name = data['name']
  speeds.append(speed)
  cities.append(name)
##storing in dictionary
dict_1 = {cities[1]: speeds[1] for i in range(len(cities))}

##creating gauge chart
my_layout = Layout(title = 'Windspeed of Montreal')

data = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = 0.51,
    mode = "gauge+number+delta",
    title = {'text': "Speed"},
    gauge = {'axis': {'range': [None, 10]},
             'steps' : [
                 {'range': [0, 20], 'color': "lightgray"},
                 {'range': [10, 50], 'color': "gray"}],
             'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))

fig = {'data': data, 'layout': my_layout}

offline.plot(fig, filename = 'windspeed.html')