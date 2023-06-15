from mvc.controller import Controller
from mvc.view import MainView
from mvc.model import Model
import threading
import time
import flet as ft
from flet import theme


def update_ui(view, model):
    while True:
        view.item_list.update()
        view.cart.update()
        time.sleep(0.1)


def main(page):
    # MVC set-up
    model = Model()
    controller = Controller(page, model)
    view = MainView(controller, model)

    light_color_scheme = ft.ColorScheme(
        primary="#ffffff",
        on_primary="#383838",
        primary_container="#737373",
        on_primary_container="#d9d9d9",
        # secondary='#4a6267',
        # on_secondary="#ffffff",
        # secondary_container="#cde7ec",
        # on_secondary_container="#051f23",
        # tertiary="#525e7d",
        # on_tertiary="#ffffff",
        # tertiary_container="#dae2ff",
        # on_tertiary_container="#0e1b37",
        error="#ba1a1a",
        error_container="#ffdad6",
        on_error="#ffffff",
        on_error_container="#410002",
        # background="#fafdfd",
        # on_background="#191c1d",
        surface="#d9d9d9",
        on_surface="#a8a8a8",
        # surface_variant="#dbe4e6",
        # on_surface_variant="#3f484a",
        outline="#383838",
    )

    dark_color_scheme = ft.ColorScheme(
        primary="#4fd8eb",
        on_primary="#00363d",
        primary_container="#004f58",
        on_primary_container="#97f0ff",
        secondary='#b1cbd0',
        on_secondary="#1c3438",
        secondary_container="#334b4f",
        on_secondary_container="#cde7ec",
        tertiary="#bac6ea",
        on_tertiary="#24304d",
        tertiary_container="#3b4664",
        on_tertiary_container="#dae2ff",
        error="#ffb4ab",
        error_container="#93000a",
        on_error="#690005",
        on_error_container="#ffdad6",
        background="#191c1d",
        on_background="#e1e3e3",
        surface="#191c1d",
        on_surface="#e1e3e3",
        surface_variant="#3f484a",
        on_surface_variant="#bfc8ca",
        outline="#899294",
    )

    # view.item_list.update()

    # model operations
    # model.controller = controller
    # model.create_checkboxes()

    # Settings
    page.on_keyboard_event = controller.on_keyboard

    # window size
    WIDTH = 1000
    HEIGHT = 700

    page.title = "University Pizza POS"

    page.window_width = WIDTH
    page.window_height = HEIGHT
    page.window_max_width = WIDTH
    page.window_max_height = HEIGHT
    page.window_min_width = WIDTH
    page.window_min_height = HEIGHT

    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    page.theme = theme.Theme(color_scheme=light_color_scheme)
    # page.theme = theme.Theme(color_scheme_seed='grey')
    page.bgcolor = ft.colors.SURFACE

    # page.window_always_on_top = True

    # Run
    page.add(*view.content)

    thread = threading.Thread(target=update_ui(view, model))
    thread.daemon = True
    thread.start()

    page.update()


ft.app(target=main, assets_dir="assets")
