from mvc.controller import Controller
from mvc.view import MainView
from mvc.model import Model
import threading
import time
import flet as ft


def update_ui(view, model):
    while True:
        view.item_list.update()
        view.cart.update()
        # view.cart.controls[0].content.controls
        # model.cart_list_view.current.controls
        time.sleep(0.1)


def main(page):
    # MVC set-up
    model = Model()
    controller = Controller(page, model)
    view = MainView(controller, model)

    # view.item_list.update()

    # model operations
    # model.controller = controller
    # model.create_checkboxes()

    # Settings
    page.on_keyboard_event = controller.on_keyboard

    # window size
    WIDTH = 1000
    HEIGHT = 700

    page.title = "Menu App UI Design"

    page.window_width = WIDTH
    page.window_height = HEIGHT
    page.window_max_width = WIDTH
    page.window_max_height = HEIGHT
    page.window_min_width = WIDTH
    page.window_min_height = HEIGHT

    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # page.window_always_on_top = True

    # Run
    page.add(
        *view.content
    )

    thread = threading.Thread(target=update_ui(view, model))
    thread.daemon = True
    thread.start()
    page.update()


ft.app(target=main)
