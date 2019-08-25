#!/usr/local/bin/python3
import random

data = [
  {'name':'Alabama','pop':4500000,'area':51000},
  {'name':'Alaska','pop':550000,'area':550000},
  {'name':'Arizona','pop':6500000,'area':110000},
  {'name':'Arkansas','pop':2000000,'area':35000},
  {'name':'California','pop':40000000,'area':150000},
  {'name':'Colorado','pop':5500000,'area':104000},
  {'name':'Connecticut','pop':3800000,'area':8000},
  {'name':'Washington','pop':7500000,'area':73000}
]

def abs_frac(x,y):
  if x > y:
    return 100.0*y/x
  return  100.0*x/y

total = 0.0
guesses = 0

for state in random.sample(data,5):
  print(state['name'])
  pop = int(input('population: '))
  area = int(input('area: '))
  guesses += 2
  total += abs_frac(pop, state['pop']) + abs_frac(area, state['area'])
  print(total/guesses)

print('done')