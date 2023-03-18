""" Flet Search Bar """
# modules
import flet as ft
import flet
from flet import *

# getting the data from somewhere for the search bar function


class DropdownSearchBar(ft.UserControl):
    def __init__(self, parent_controller):
        # <- NOTE: see how I save the controller here
        self.parent_controller = parent_controller
        self.item_number = ft.Text(size=9, italic=True,
                                   color="white54")
        self.item_number.value = "search results:"
        super().__init__()

    def drop_down_search(self):
        _object_ = ft.Container(
            # width=450,
            height=50,
            bgcolor='black',
            border_radius=10,
            padding=ft.padding.only(top=15, left=21, right=21, bottom=15),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,  # making sure there is no overflow
            animate=ft.animation.Animation(400, 'decelerate'),
            content=ft.Column(  # This is where things will be stored
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,
                controls=[  # This is where the search field is located
                    ft.Row(
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.icons.SEARCH_ROUNDED,
                                    size=15, opacity=0.90),
                            ft.TextField(
                                border_color='transparent',
                                height=20,
                                expand=True,
                                text_size=12,
                                content_padding=2,
                                cursor_color='white',
                                cursor_width=1,
                                hint_text='Search ...',
                                on_change=lambda e: (self.parent_controller.filter_search_items(
                                    e, result=self.item_number), self.update()),
                            ),
                            self.item_number,
                        ]
                    ),
                ]
            )
        )

        return _object_

    # this main build return
    def build(self):
        return self.drop_down_search()
