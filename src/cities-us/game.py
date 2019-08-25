import json
import math
import sys
from collections import defaultdict

def print_score(scoreboard, factor):
  idx = 50
  complete = 0
  scores = [(k, len(v)) for k, v in scoreboard.iteritems() if len(v) > 0]
  for state, score in sorted(scores, key=lambda x: x[1], reverse=True):
    target = int(math.ceil(idx/float(factor)))
    checkmark = ''
    if score >= target:
      checkmark = '*'
      complete += 1
    print '%s: %d/%d %s' % (state, score, target, checkmark)
    idx -= 1
  idx = 1
  overall = 0
  for score in sorted([x[1] for x in scores]):
    if score >= math.ceil(idx/float(factor)):
      overall += 1
    idx += 1
  print '%d/50' % overall

def print_done(scoreboard, data):
  for state in sorted(data.iterkeys()):
    print '%s: %d' % (state, len(scoreboard[state]))

def print_this(scoreboard, state):
  print '%s: %s' % (state, sorted(scoreboard[state]))

def print_left(data):
  for state, cities in sorted(data.iteritems()):
    print state, len(cities)

with open('cities.json', 'rb') as infile:
  data = json.loads(infile.read())

factor = 5
score = defaultdict(list)
if len(sys.argv) > 1:
  factor = int(sys.argv[1])
current_state = ''

while True:
  line = raw_input('> ')
  if line.startswith(':'):
    cmd = line[1:]
    if cmd == 'quit':
      print_score(score, factor)
      break
    if cmd == 'score':
      print_score(score, factor)
      continue
    if cmd == 'show all':
      print_done(score, data)
      continue
    if cmd == 'show this':
      print_this(score, current_state)
      continue
    if cmd == 'left':
      print_left(data)
      continue
    current_state = cmd
  else:
    city = line.strip()
    cities = data.get(current_state)
    if not cities:
      print 'No cities left for %s' % current_state
      continue
    if city in cities:
      score[current_state].append(city)
      print '%s: %d +' % (current_state, len(score[current_state]))
      data[current_state].remove(city)
    else:
      print '%s: %d' % (current_state, len(score[current_state]))

print 'done'