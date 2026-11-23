
from ursina import *
from config import ROAD_WIDTH, TRACK_LENGTH
import random


class Track:

    def __init__(self, map_data):
        self.map_data = map_data
        self.entities = []
        self.build()

    def add(self, **kwargs):
        entity = Entity(**kwargs)
        self.entities.append(entity)
        return entity

    def build(self):

        # =========================
        # ЗЕМЛЯ
        # =========================

        self.add(
            model="plane",
            scale=(260, 1, 1000),
            position=(0, -0.2, 200),
            color=self.map_data["ground"]
        )

        # =========================
        # АСФАЛЬТОВАЯ ДОРОГА
        # =========================

        self.add(
            model="cube",
            scale=(ROAD_WIDTH, 0.25, TRACK_LENGTH + 180),
            position=(0, 0, 200),
            color=self.map_data["road"]
        )

        # Обочины
        for x in [-ROAD_WIDTH / 2 - 1, ROAD_WIDTH / 2 + 1]:

            self.add(
                model="cube",
                scale=(2, 0.3, TRACK_LENGTH + 180),
                position=(x, 0.05, 200),
                color=color.rgb(110, 110, 110)
            )

        # Краевые линии
        for x in [-ROAD_WIDTH / 2 + 0.4, ROAD_WIDTH / 2 - 0.4]:

            self.add(
                model="cube",
                scale=(0.25, 0.04, TRACK_LENGTH + 180),
                position=(x, 0.16, 200),
                color=color.white
            )

        # Центральная разметка
        for z in range(-40, TRACK_LENGTH + 150, 12):

            self.add(
                model="cube",
                scale=(0.22, 0.05, 5),
                position=(0, 0.17, z),
                color=color.yellow
            )

        # =========================
        # ОГРАЖДЕНИЯ
        # =========================

        for side in [-1, 1]:

            x = side * (ROAD_WIDTH / 2 + 2)

            self.add(
                model="cube",
                scale=(0.3, 0.8, TRACK_LENGTH + 150),
                position=(x, 0.5, 200),
                color=color.rgb(180, 185, 195)
            )

            # Стойки ограждения
            for z in range(-40, TRACK_LENGTH + 150, 10):

                self.add(
                    model="cube",
                    scale=(0.45, 1.1, 0.5),
                    position=(x, 0.5, z),
                    color=color.dark_gray
                )

        # =========================
        # ЗДАНИЯ
        # =========================

        for z in range(-20, TRACK_LENGTH + 100, 35):

            for side in [-1, 1]:

                x = side * random.uniform(23, 35)

                height = random.uniform(8, 22)
                width = random.uniform(8, 14)
                depth = random.uniform(9, 16)

                building_color = random.choice([
                    color.rgb(100, 110, 130),
                    color.rgb(130, 135, 145),
                    color.rgb(75, 85, 105),
                    color.rgb(155, 145, 130),
                    color.rgb(85, 100, 120)
                ])

                # Основное здание
                self.add(
                    model="cube",
                    scale=(width, height, depth),
                    position=(x, height / 2, z),
                    color=building_color
                )

                # Крыша
                self.add(
                    model="cube",
                    scale=(width + 0.5, 0.4, depth + 0.5),
                    position=(x, height + 0.2, z),
                    color=color.dark_gray
                )

                # Окна
                for floor in range(1, int(height // 3) + 1):

                    for window_x in [-width / 4, width / 4]:

                        self.add(
                            model="cube",
                            scale=(1.3, 1.5, 0.12),
                            position=(
                                x + window_x,
                                floor * 3,
                                z + depth / 2 + 0.08
                            ),
                            color=color.rgb(110, 190, 235)
                        )

        # =========================
        # ДЕРЕВЬЯ
        # =========================

        for z in range(-35, TRACK_LENGTH + 130, 15):

            for side in [-1, 1]:

                x = side * random.uniform(14, 21)

                tree_height = random.uniform(3, 5)

                # Ствол
                self.add(
                    model="cylinder",
                    scale=(0.45, tree_height, 0.45),
                    position=(x, tree_height / 2, z),
                    color=color.rgb(105, 65, 35)
                )

                # Крона
                self.add(
                    model="sphere",
                    scale=(3, 4, 3),
                    position=(x, tree_height + 1.2, z),
                    color=random.choice([
                        color.rgb(35, 115, 45),
                        color.rgb(45, 140, 55),
                        color.rgb(65, 125, 40)
                    ])
                )

        # =========================
        # СТАРТОВАЯ ЛИНИЯ
        # =========================

        start_z = -10

        # Шахматная разметка
        tile_size = 1

        for row in range(2):
            for col in range(ROAD_WIDTH):

                tile_color = (
                    color.white
                    if (row + col) % 2 == 0
                    else color.black
                )

                self.add(
                    model="cube",
                    scale=(tile_size, 0.06, tile_size),
                    position=(
                        -ROAD_WIDTH / 2 + col + 0.5,
                        0.17,
                        start_z + row
                    ),
                    color=tile_color
                )

        self.create_arch(start_z, "START", color.azure)

        # =========================
        # ФИНИШНАЯ ЛИНИЯ
        # =========================

        finish_z = TRACK_LENGTH

        for row in range(2):
            for col in range(ROAD_WIDTH):

                tile_color = (
                    color.white
                    if (row + col) % 2 == 0
                    else color.black
                )

                self.add(
                    model="cube",
                    scale=(tile_size, 0.06, tile_size),
                    position=(
                        -ROAD_WIDTH / 2 + col + 0.5,
                        0.18,
                        finish_z + row
                    ),
                    color=tile_color
                )

        self.create_arch(
            finish_z,
            "FINISH",
            color.orange
        )

    # =========================
    # АРКА СТАРТА И ФИНИША
    # =========================

    def create_arch(self, z, label, arch_color):

        height = 7
        width = ROAD_WIDTH + 2

        # Левая опора
        self.add(
            model="cube",
            scale=(0.8, height, 0.8),
            position=(-width / 2, height / 2, z),
            color=arch_color
        )

        # Правая опора
        self.add(
            model="cube",
            scale=(0.8, height, 0.8),
            position=(width / 2, height / 2, z),
            color=arch_color
        )

        # Верхняя балка
        self.add(
            model="cube",
            scale=(width + 0.8, 1.2, 1),
            position=(0, height, z),
            color=arch_color
        )

        # Табличка
        self.add(
            model="cube",
            scale=(7, 1.5, 0.3),
            position=(0, height, z + 0.6),
            color=color.rgb(20, 25, 40)
        )

        # Надпись
        text_entity = Text(
            text=label,
            parent=scene,
            position=(0, height - 0.25, z + 0.85),
            origin=(0, 0),
            scale=4,
            color=color.white
        )

        self.entities.append(text_entity)
