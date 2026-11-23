from ursina import *

TITLE = "MICRO RACING"
WINDOW_SIZE = (1280, 720)
ROAD_WIDTH = 18
TRACK_LENGTH = 420
CAR_COLORS = [color.azure, color.orange, color.lime, color.red, color.violet]
CARS = [
    {"name": "Comet", "speed": 34, "acceleration": 18, "handling": 105, "price": 0},
    {"name": "Blaze", "speed": 39, "acceleration": 20, "handling": 98, "price": 350},
    {"name": "Phantom", "speed": 44, "acceleration": 22, "handling": 92, "price": 700},
]
MAPS = [
    {"name": "Green Valley", "sky": color.rgb(125, 190, 235), "ground": color.rgb(65, 145, 75), "road": color.rgb(55, 58, 65)},
    {"name": "Desert Run", "sky": color.rgb(245, 174, 105), "ground": color.rgb(190, 145, 85), "road": color.rgb(65, 63, 61)},
    {"name": "Neon City", "sky": color.rgb(22, 25, 52), "ground": color.rgb(35, 38, 55), "road": color.rgb(43, 45, 60)},
]
