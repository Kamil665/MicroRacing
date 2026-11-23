from ursina import *
from config import CARS
from save_system import save_save

class Garage:
    def __init__(self, app):
        self.app = app
        self.panel = Entity(parent=camera.ui, model="quad", scale=(.78, .72),
                            color=color.rgba(15, 20, 32, 245), enabled=False)
        self.title = Text("GARAGE", parent=self.panel, y=.38, origin=(0, 0), scale=2)
        self.car_name = Text("", parent=self.panel, y=.12, origin=(0, 0), scale=1.5)
        self.info = Text("", parent=self.panel, y=-.02, origin=(0, 0))
        self.prev = Button("‹", parent=self.panel, x=-.28, y=-.18, scale=(.12, .1))
        self.next = Button("›", parent=self.panel, x=.28, y=-.18, scale=(.12, .1))
        self.buy = Button("SELECT", parent=self.panel, y=-.34, scale=(.3, .1))
        self.close = Button("CLOSE", parent=self.panel, x=.34, y=.38, scale=(.18, .08))
        self.prev.on_click = self.previous
        self.next.on_click = self.next_car
        self.buy.on_click = self.select
        self.close.on_click = self.hide
        self.index = app.save["selected_car"]

    def show(self):
        self.panel.enabled = True
        self.refresh()

    def hide(self):
        self.panel.enabled = False

    def previous(self):
        self.index = (self.index - 1) % len(CARS)
        self.refresh()

    def next_car(self):
        self.index = (self.index + 1) % len(CARS)
        self.refresh()

    def refresh(self):
        car = CARS[self.index]
        unlocked = self.index in self.app.save["unlocked_cars"]
        self.car_name.text = car["name"]
        self.info.text = f'Max speed: {car["speed"]}   Acceleration: {car["acceleration"]}\\nPrice: {car["price"]} coins'
        self.buy.text = "SELECTED" if self.app.save["selected_car"] == self.index else ("SELECT" if unlocked else "BUY")

    def select(self):
        car = CARS[self.index]
        if self.index not in self.app.save["unlocked_cars"]:
            if self.app.save["coins"] < car["price"]:
                self.info.text = "Not enough coins!"
                return
            self.app.save["coins"] -= car["price"]
            self.app.save["unlocked_cars"].append(self.index)
        self.app.save["selected_car"] = self.index
        save_save(self.app.save)
        self.refresh()
