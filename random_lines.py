import random

from draw import draw, start_with_time

res = 500

start_with_time(2)
for _ in range(10000):
    draw(random.randint(-res, res), random.randint(-res, res))