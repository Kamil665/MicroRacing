from ursina import *
import random
from car import Car

class Bot(Car):
    def __init__(self, position, lane, difficulty=1.0):
        palette = [color.red, color.orange, color.violet, color.lime]
        stats = {"speed": random.uniform(25, 31) * difficulty,
                 "acceleration": 15, "handling": 65}
        super().__init__(position=position, car_color=random.choice(palette), stats=stats)
        self.lane = lane
        self.phase = random.random() * 6
        self.target_speed = stats["speed"]

    def update_bot(self, dt, player_z):
        if self.z < player_z - 35:
            self.z = player_z + random.uniform(22, 35)
            self.x = self.lane + random.uniform(-1.2, 1.2)
            self.velocity = 0
        self.velocity = min(self.target_speed, self.velocity + self.acceleration * dt)
        self.phase += dt
        self.x += sin(self.phase) * .35 * dt
        self.z -= 0  # Bots travel in the same forward direction as the player.
        self.position += self.forward * self.velocity * dt
