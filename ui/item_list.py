from flet import Container, Column, MainAxisAlignment, colors, UserControl, Text, alignment, ListView, padding, Row, CrossAxisAlignment, BoxShape, Icon, icons, GridView, ResponsiveRow
import asyncio
from ui.item import Item


class ItemList(UserControl):
    def __init__(self, model, controller):
        self.parent_controller = controller
        self.model = model
        super().__init__()

    def build(self):
        menu_items = self.model.menu()
        menu_column = GridView(
            controls=self.parent_controller.items(
                menu_items, self.parent_controller),
            ref=self.model.menu_list_view,
            spacing=10,
            padding=10,
            runs_count=2,
            child_aspect_ratio=1.5
        )
        container = Container(
            content=menu_column,
            border_radius=10,
            bgcolor='black',
            height=self.model.HEIGHT*0.9,
        )
        return container
