#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt

def go_from(a, b):
  x0, y0 = a
  x1, y1 = b
  diff_x = x1 - x0
  diff_y = y1 - y0
  ans = []
  if diff_x == 0 and diff_y == 0:
    # both are same point
    pass
  elif diff_x == 0:
    # vertical line
    unit = diff_y / abs(diff_y)
    ans.append([x0, y0])
    while y0 != y1:
      y0 += unit
      ans.append([x0, y0])
  else:
    unit_y = float(diff_y) / abs(diff_x)
    unit_x = diff_x / abs(diff_x)
    start_y = y0
    ans.append([x0, y0])
    while x0 != x1:
      x0 += unit_x
      y0 += unit_y
      if abs(x0 * diff_y) % abs(diff_x) == 0:
          ans.append([x0, y0])
  return map(lambda p: map(int, p), ans)
  
  
def distance(x, y):
  x1, y1, x2, y2 = x + y
  # √ (x2 - x1) ^ 2 + (y2 - y1) ^ 2
  xdiff, ydiff = x2 - x1, y2 - y1
  return sqrt(xdiff * xdiff + ydiff * ydiff + 0.0)

def line_equation(x, y):
  # y = mx + c
  # y1 = m * x1 + c
  # y2 = m * x2 + c
  # m = (y2 - y1) / (x2 - x1)
  # c = (y1 * x2 - y2 * x1) / (x2 - x1)
  x1, y1, x2, y2 = x + y
  slope = (y2 - y1) / (x2 - x1 + 0.0)
  constant =  (y1 * x2 - y2 * x1) / (x2 - x1 + 0.0)
  return (slope, constant)
  

def draw_scaled(real_grid, screen_x, screen_y=None):
  if not screen_y:
    screen_y = screen_x
  magnification_x = len(real_grid) / screen_x
  if magnification_x == 0:
    magnification_x = 1
  magnification_y = len(real_grid) / screen_y
  if magnification_y == 0:
    magnification_y = 1
  for i in xrange(0, len(real_grid), magnification_x):
    for j in xrange(0, len(real_grid[0]), magnification_y):
      print real_grid[i][j],
    print '.'

real_n = 1.0
precision = 10 ** (-2)
n = int(real_n / precision)
found = False


grid = [[' ' for _ in range(n)] for __ in range(n)]

o1_x1 = int(0.3 * real_n * n)
o1_x2 = int(0.5 * real_n * n)
o1_y1 = int(0.2 * real_n * n)
o1_y2 = int(0.8 * real_n * n)

for i in range(o1_x1, o1_x2+1):
	for j in range(o1_y1, o1_y2+1):
		grid[i][j] = 'X'
		
'''		
for i in xrange(35, 26):
  for j in xrange(50, 76):
    grid[i][j] = ' '
'''		

for i in range(n):
  for j in range(n):
    if i in (0, n-1) or j in (0, n-1):
      grid[i][j] = '.'

# start
start = 0.7 * real_n, 0.9 * real_n
#goal
goal =  0.2 * real_n, 0.4 * real_n

start = [int(x * n) for x in start]
goal =  [int(y * n) for y in goal]

grid[start[0]][start[1]] = 'S' 
grid[goal[0]][goal[1]] = 'G'

m, c = line_equation(start, goal)

hit_points = []
leave_points = []

x, y = start
while True:
  if [x, y] == goal:
    break
  tail = [x, y]
  
  next_x = x - 1
  next_y = y - 1
  
  next_leave_point = None
  distance_to_goal = 10 ** 9 

  
  if grid[next_x][next_y] == 'X':
    hit_points.append([next_x, next_y])
    # next_x, next_y is a hit point
    # grid[next_x][next_y] = '$'
    initial_possibilties = []
    for i in xrange(-1, 2):
      for j in xrange(-1, 2):
        if grid[next_x+i][next_y+j] not in 'X*':
          initial_possibilties.append([next_x+i, next_y+j])
    possibilities_with_distances = map(lambda point: [point, distance(hit_points[-1], point)], initial_possibilties)
    possibilities_with_distances.sort(key=lambda x: x[1])
    initial_point = possibilities_with_distances[0][0]
    grid[initial_point[0]][initial_point[1]] = '*'
    obs_point = [next_x, next_y]
    graze_point = [initial_point[0], initial_point[1]]

    next_possible_graze_points = []
    next_possible_obs_points = []
    
    while True:
      next_possible_graze_points = []
      next_possible_obs_points = []
      for i in xrange(-1, 2):
        for j in xrange(-1, 2):
          if grid[obs_point[0]+i][obs_point[1]+j] not in 'X*':
            next_possible_graze_points.append([obs_point[0]+i, obs_point[1]+j])

      if not next_possible_graze_points:
        break
      
      next_possible_graze_points = [sorted(map(lambda point: [point, distance(point, obs_point)], next_possible_graze_points), key=lambda x:x[1])[0][0]]
      
      
      if len(next_possible_graze_points) == 1:
        graze_point = next_possible_graze_points[0]
        grid[graze_point[0]][graze_point[1]] = '*'
        for m in xrange(-1, 2):
          for n in xrange(-1, 2):
            if grid[graze_point[0]+m][graze_point[1]+n] == 'X':
              next_possible_obs_points.append([graze_point[0]+m, graze_point[1]+n])
        next_possible_obs_points = map(lambda point: [point, distance(point, graze_point)], next_possible_obs_points)
        next_possible_obs_points.sort(key=lambda x:x[1])
        obs_point = next_possible_obs_points[0][0]
        if not next_leave_point:
          next_leave_point = graze_point
        tmp = distance(graze_point, goal)
        if tmp < distance_to_goal:
          next_leave_point = graze_point
          distance_to_goal = tmp
          
      else:
        for point in next_possible_graze_points:
          grid[point[0]][point[1]] = '?'
    
    path = go_from(next_leave_point, goal)
    for (x, y) in path[:-1]:
      grid[x][y] = '*'
    
    if path[-1] == goal:
      found = True
      break

  else:
    x, y = next_x, next_y
    grid[x][y] = '*'
  
    
draw_scaled(grid, 100)

if found:
  print "PATH FOUND BETWEEN START AND GOAL"
else:
  print "NO PATH FROM START To GOAL"