from ursina import *
from config import *
from car import Car
from bot import Bot
from track import Track
from garage import Garage
from ui import GameUI
from save_system import load_save, save_save
import random

app = Ursina()
window.title = TITLE
window.borderless = False
window.fullscreen = False
window.size = WINDOW_SIZE
window.color = color.rgb(100, 160, 210)
window.exit_button.visible = False
mouse.visible = True

class MicroRacing:
    def __init__(self):
        self.save = load_save()
        self.state = "menu"
        self.track = None
        self.player = None
        self.player2 = None
        self.bots = []
        self.elapsed = 0
        self.multiplayer = False
        self.map_index = self.save["selected_map"]
        self.menu_entities = []
        # Сначала создаём интерфейс
        self.ui = GameUI()
        # Затем гараж
        self.garage = Garage(self)
        # И только после этого главное меню
        self.make_menu()
        self.set_hud(False)

    def make_menu(self):
        self.menu_bg = Entity(parent=camera.ui, model="quad", scale=(2, 1.2),
                              color=color.rgba(8, 13, 28, 240), z=1)
        self.menu_title = Text("MICRO RACING", parent=camera.ui, y=.28,
                               origin=(0, 0), scale=3, color=color.azure)
        self.menu_sub = Text("3D ARCADE RACING", parent=camera.ui, y=.19,
                             origin=(0, 0), scale=1)
        self.play_btn = Button("RACE", parent=camera.ui, y=.06, scale=(.28, .075))
        self.two_btn = Button("LOCAL MULTIPLAYER", parent=camera.ui, y=-.04, scale=(.28, .075))
        self.garage_btn = Button("GARAGE", parent=camera.ui, y=-.14, scale=(.28, .075))
        self.map_btn = Button("MAP: GREEN VALLEY", parent=camera.ui, y=-.24, scale=(.28, .075))
        self.quit_btn = Button("QUIT", parent=camera.ui, y=-.34, scale=(.28, .075))
        self.coins_text = Text("", parent=camera.ui, y=-.44, origin=(0, 0), scale=1)
        self.play_btn.on_click = lambda: self.start_race(False)
        self.two_btn.on_click = lambda: self.start_race(True)
        self.garage_btn.on_click = self.garage.show
        self.map_btn.on_click = self.next_map
        self.quit_btn.on_click = application.quit
        self.refresh_menu()

    def refresh_menu(self):
        self.coins_text.text = f'COINS: {self.save["coins"]}'
        self.map_btn.text = "MAP: " + MAPS[self.map_index]["name"].upper()

    def next_map(self):
        self.map_index = (self.map_index + 1) % len(MAPS)
        self.save["selected_map"] = self.map_index
        save_save(self.save)
        self.refresh_menu()

    def set_hud(self, enabled):
        for obj in (self.ui.speed, self.ui.position, self.ui.timer,
                    self.ui.nitro_label, self.ui.nitro_bg, self.ui.nitro_bar):
            obj.enabled = enabled

    def start_race(self, multiplayer):
        self.multiplayer = multiplayer
        self.state = "race"
        self.elapsed = 0
        self.menu_bg.enabled = False
        for obj in (self.menu_title, self.menu_sub, self.play_btn, self.two_btn,
                    self.garage_btn, self.map_btn, self.quit_btn, self.coins_text):
            obj.enabled = False
        self.garage.hide()
        self.track = Track(MAPS[self.map_index])
        car_data = CARS[self.save["selected_car"]]
        self.player = Car(
            position=(-2.5, 0.55, -25),
            car_color=color.azure,
            stats=car_data
        )
        self.player2 = Car(position=(2.5, .55, -31), car_color=color.orange,
                           stats={"speed": 32, "acceleration": 17, "handling": 100}, player=2) if multiplayer else None
        self.bots = []

        bot_positions = [
            (2.5, 0.55, -25),  # Справа от игрока
            (-6, 0.55, -31),  # Слева и немного позади
            (6, 0.55, -31),  # Справа и немного позади
            (0, 0.55, -37),  # Позади по центру
        ]

        for position in bot_positions:
            bot = Bot(
                position=position,
                lane=position[0]
            )
            self.bots.append(bot)

        self.ui.message.enabled = False
        self.set_hud(True)
        camera.position = (0, 10, -48)
        camera.rotation = (12, 0, 0)
        camera.fov = 90
        self.pause_text = Text("PAUSED", origin=(0, 0), scale=3, enabled=False)

    def end_race(self):
        self.state = "results"
        self.player.velocity = 0
        self.set_hud(False)
        self.ui.message.text = f"FINISH! TIME: {int(self.elapsed)} sec. 100 COINS. ENTER - MENU"
        self.ui.message.color = color.black
        self.ui.message.enabled = True
        self.save["coins"] += 100
        if self.save["best_time"] is None or self.elapsed < self.save["best_time"]:
            self.save["best_time"] = round(self.elapsed, 2)
        save_save(self.save)

    def return_menu(self):
        self.state = "menu"
        destroy(self.track_root) if hasattr(self, "track_root") else None
        if self.track:
            for entity in self.track.entities:
                destroy(entity)
        if self.player: destroy(self.player)
        if self.player2: destroy(self.player2)
        for bot in self.bots: destroy(bot)
        self.player = self.player2 = None
        self.bots = []
        self.ui.message.enabled = False
        self.menu_bg.enabled = True
        for obj in (self.menu_title, self.menu_sub, self.play_btn, self.two_btn,
                    self.garage_btn, self.map_btn, self.quit_btn, self.coins_text):
            obj.enabled = True
        self.refresh_menu()
        camera.position = (0, 0, -20)
        camera.rotation = (0, 0, 0)

    def update(self):
        if self.state != "race":
            return

        dt = time.dt
        self.elapsed += dt

        keys = held_keys

        # УПРАВЛЕНИЕ ИГРОКОМ 1
        self.player.drive(
            int(keys["w"] or keys["up"]),
            int(keys["d"]) - int(keys["a"]),
            keys["s"] or keys["down"],
            dt,
            keys["space"]
        )

        # УПРАВЛЕНИЕ ИГРОКОМ 2
        if self.player2:
            self.player2.drive(
                int(keys["i"]),
                int(keys["l"]) - int(keys["j"]),
                keys["k"],
                dt,
                keys["right shift"]
            )

            self.player2.z = max(
                self.player2.z,
                self.player.z - 18
            )

        # ДВИЖЕНИЕ СОПЕРНИКОВ
        for bot in self.bots:
            bot.update_bot(dt, self.player.z)

            if distance(bot.position, self.player.position) < 2.5:
                self.player.velocity *= 0.55
                bot.z += 6

        # КАМЕРА ОТ ТРЕТЬЕГО ЛИЦА
        target_camera = Vec3(
            self.player.x * 0.45,
            10,
            self.player.z - 24
        )

        camera.position = lerp(
            camera.position,
            target_camera,
            min(1, dt * 5)
        )

        camera.look_at(
            self.player.position + Vec3(0, 0, 15)
        )

        # ПОЗИЦИЯ В ГОНКЕ
        place = 1 + sum(
            1 for bot in self.bots
            if bot.z > self.player.z
        )

        self.ui.update_hud(
            self.player,
            self.elapsed,
            place,
            len(self.bots) + 1
        )

        # ФИНИШ
        if self.player.z >= TRACK_LENGTH:
            self.end_race()


game = MicroRacing()


# Главный игровой цикл Ursina
def update():
    game.update()


def input(key):
    if key == "escape":
        if game.state == "race":
            game.state = "paused"
            game.pause_text.enabled = True
            game.set_hud(False)

        elif game.state == "paused":
            game.state = "race"
            game.pause_text.enabled = False
            game.set_hud(True)

        elif game.state == "results":
            game.return_menu()

        elif game.state == "menu":
            application.quit()

    if key == "enter" and game.state == "results":
        game.return_menu()

    if key == "enter" and game.state == "paused":
        game.state = "race"
        game.pause_text.enabled = False
        game.set_hud(True)


app.run()
