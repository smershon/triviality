import csv
from collections import defaultdict
import json
import yaml

state_ids = set([
  'AL', 'AK', 'AR', 'AZ',
  'CA', 'CO', 'CT',
  'DE', 'FL', 'GA', 'HI',
  'ID', 'IA', 'IL', 'IN',
  'KS', 'KY', 'LA',
  'ME', 'MA', 'MD', 'MI', 'MN', 'MS', 'MO', 'MT',
  'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND',
  'OH', 'OK', 'OR',
  'PA', 'RI', 'SC', 'SD',
  'TN', 'TX', 'UT',
  'VA', 'VT',
  'WA', 'WV', 'WI', 'WY'])

class Ranker:
  def __init__(self):
    self.data = defaultdict(int)

  def rank(self, label):
    self.data[label] += 1
    return self.data[label]

def qualify(city):
  return (city['rank']['overall'] <= 1000 
    or city['rank']['by_state'] <= 50
    or (city['rank']['by_name'] <= 1 and city['rank']['overall'] <= 5000))

data = []

stream = file('overrides.yaml', 'rb')
overrides = yaml.load(stream)
stream.close()

with open('cities.csv', 'rb') as infile:
  reader = csv.DictReader(infile)
  for row in reader:
    state = row['state_id']
    city = row['city_ascii']
    if state not in state_ids:
      continue
    population = 0
    if row['population_proper'] != '':
      population = int(row['population_proper'])
    if state in overrides and city in overrides[state]:
      population = overrides[state][city]
    if population > 0:
      data.append({
        'name': city, 
        'state': state, 
        'pop': population,
        'id': int(row['id'])})

data.sort(key=lambda x: x['pop'], reverse=True)

overall = Ranker()
by_state = Ranker()
by_name = Ranker()
state_data = defaultdict(list)

for city in data:
  city['rank'] = {
    'overall': overall.rank(''),
    'by_state': by_state.rank(city['state']),
    'by_name': by_name.rank(city['name'])
  }
  if qualify(city):
    state_data[city['state']].append(city)

output = {}

for state, cities in sorted(state_data.iteritems()):
  output[state] = [x['name'] for x in cities]

with open('cities.json', 'wb') as outfile:
  outfile.write(json.dumps(output))
