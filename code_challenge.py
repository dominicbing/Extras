# Gathering the Data
from urllib.request import urlopen
import calendar
import datetime
import json

request  = urlopen("https://api.coinranking.com/v1/public/coin/1/history/30d")
response = request.read()
text = json.loads(response)
        
    
# Convert UTC to Actual Time
date_fix = []
for i in text['data']['history']:
  i['timestamp'] = str(datetime.datetime.fromtimestamp(int(str(i['timestamp'])[:10])))
  date_fix.append(i)


# Making Timestamps show only "T00:00:00"
for i in date_fix:
  i['timestamp'] = i['timestamp'][:10] + "T00:00:00"
  i['price'] = float(i['price'])
  

# Gathering list of distinct dates
time_list = []
for i in date_fix:
  time_list.append(i['timestamp'])
  
time_set = set(time_list)
time_set_list = []
for i in time_set:
  time_set_list.append(i)
  
time_set_list_sorted = sorted(time_set_list)


# Gathering the sum of prices per day
run = 0
new_sum = 0
max_run = len(time_set_list_sorted) - 1

new_list = []

while run <= max_run:
  for i in date_fix:
    if time_set_list_sorted[run] == i['timestamp']:
      new_sum += i['price']
  
  new_dict = {}
  new_dict['timestamp'] = time_set_list_sorted[run]
  new_dict['price'] = new_sum
  
  new_list.append(new_dict)
  
  new_sum = 0
  run += 1
  

# Creating Weekday, highest, and lowest columns
for i in new_list:
  i['dayOfWeek'] = calendar.day_name[datetime.datetime.strptime(i['timestamp'], '%Y-%m-%dT%H:%M:%S').weekday()]
  i['highSinceStart'] = 'False'
  i['lowSinceStart'] = 'False'

  
# Creating the Direction, Price Change Columns
run = 0
max_run = len(new_list) - 1

while run <= max_run:
  price_change = 0
  direction = ''
  
  if run == 0:
    new_list[run]['direction'] = 'na'
    new_list[run]['price_change'] = 0
    new_list[run]['highSinceStart'] = 'True'
    new_list[run]['lowSinceStart'] = 'False'
    
    new_list_max_price = new_list[run]['price']
    new_list_min_price = new_list[run]['price']
    
  else:
    price_change = new_list[run]['price'] - new_list[run - 1]['price']
  
    if price_change > 0:
      direction = 'up'
    elif price_change < 0:
      direction = 'down'
    else:
      direction = 'same'

    new_list[run]['direction'] = direction
    new_list[run]['price_change'] = price_change
    
    if new_list[run]['price'] > new_list_max_price:
      new_list_max_price = new_list[run]['price']

    if new_list[run]['price'] < new_list_min_price:
      new_list_min_price = new_list[run]['price']
    
  run += 1

for i in new_list:
  if i['price'] == new_list_max_price:
    i['highSinceStart'] = 'True'
    
  if i['price'] == new_list_min_price:
    i['lowSinceStart'] = 'True'
    
for i in new_list:
  print(i)


# Saving to JSON
out_file = open("myfile.json", "w")  
json.dump(new_list, out_file, indent = 6)  
out_file.close()  
