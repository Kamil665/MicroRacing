from ursina import *

class GameUI:
    def __init__(self):
        self.speed = Text("0 KM/H", position=(-.86, .45), scale=1.5)
        self.position = Text("POSITION 1/1", position=(-.86, .39), scale=1)
        self.timer = Text("TIME 00:00", position=(.65, .45), scale=1.2)
        self.nitro_label = Text("NITRO", position=(-.86, -.42), scale=1)
        self.nitro_bg = Entity(parent=camera.ui, model="quad", position=(-.69, -.44),
                               scale=(.25, .025), color=color.dark_gray)
        self.nitro_bar = Entity(parent=camera.ui, model="quad", origin=(-.5, 0),
                                position=(-.815, -.44), scale=(.25, .018), color=color.azure)
        self.message = Text("", origin=(0, 0), y=.1, scale=2)
        self.message.enabled = False

    def update_hud(self, car, elapsed, place, total):
        self.speed.text = f"{car.speed_kmh()} KM/H"
        self.position.text = f"POSITION {place}/{total}"
        self.timer.text = f"TIME {int(elapsed)//60:02d}:{int(elapsed)%60:02d}"
        self.nitro_bar.scale_x = .25 * car.nitro / 100
