from ursina import *
from config import ROAD_WIDTH

class Car(Entity):
    def __init__(self, position=(0, .55, 0), car_color=color.azure, stats=None, player=1):
        super().__init__(position=position)
        self.player = player
        self.stats = stats or {"speed": 34, "acceleration": 18, "handling": 105}
        self.max_speed = self.stats["speed"]
        self.acceleration = self.stats["acceleration"]
        self.handling = self.stats["handling"]
        self.velocity = 0
        self.nitro = 100
        self.nitro_active = False
        self.finished = False

        self.body = Entity(parent=self, model="cube", scale=(1.8, .55, 3.5),
                           position=(0, .35, 0), color=car_color)
        self.cabin = Entity(parent=self, model="cube", scale=(1.35, .65, 1.65),
                            position=(0, .9, -.25), color=color.rgb(35, 45, 58))
        self.wheels = []
        for x in (-.95, .95):
            for z in (-1.1, 1.1):
                wheel = Entity(parent=self, model="cylinder", scale=(.42, .22, .42),
                               position=(x, .12, z), rotation=(0, 0, 90),
                               color=color.black)
                self.wheels.append(wheel)
        self.front_lights = [
            Entity(parent=self, model="cube", scale=(.42, .12, .08),
                   position=(-.55, .42, 1.77), color=color.yellow),
            Entity(parent=self, model="cube", scale=(.42, .12, .08),
                   position=(.55, .42, 1.77), color=color.yellow),
        ]
        self.nitro_flame = Entity(parent=self, model="cone", color=color.azure,
                                  scale=(.35, .8, .35), position=(0, .3, -2.0),
                                  rotation=(90, 0, 0), enabled=False)

    def drive(self, throttle, steering, braking, dt, nitro=False):
        if self.finished:
            self.velocity = 0
            return

        # Ускорение
        target_speed = self.max_speed

        if nitro and self.nitro > 0 and throttle:
            target_speed *= 1.5

        if throttle:
            self.velocity += self.acceleration * dt
            self.velocity = min(self.velocity, target_speed)
        else:
            self.velocity = max(0, self.velocity - 7 * dt)

        if braking:
            self.velocity = max(0, self.velocity - 35 * dt)

        # Нитро
        using_nitro = nitro and throttle and self.nitro > 0

        if using_nitro:
            self.nitro = max(0, self.nitro - 35 * dt)
        else:
            self.nitro = min(100, self.nitro + 12 * dt)

        self.nitro_flame.enabled = using_nitro

        # Повороты
        steer_power = self.handling * (0.3 + self.velocity / max(1, self.max_speed))
        self.rotation_y += steering * steer_power * dt

        # Движение автомобиля
        self.position += self.forward * self.velocity * dt

        # Ограничение трассы
        self.x = clamp(self.x, -7, 7)
        self.y = 0.55

    def speed_kmh(self):
        return int(self.velocity * 3.6)
