from flet import (
    Container,
    Column,
    MainAxisAlignment,
    colors,
    UserControl,
    Text,
    alignment,
    ListView,
    padding,
    Row,
    CrossAxisAlignment,
    BoxShape,
    Icon,
    icons,
    GridView,
    ResponsiveRow,
)
import asyncio


class Item(UserControl):
    def __init__(self, text, controller):
        self.parent_controller = controller
        self.text = text
        super().__init__()

    def build(self):
        category, name, price = self.text.split(",")
        return Container(
            expand=True,
            # height=100,
            bgcolor=colors.ON_SURFACE,
            border_radius=10,
            padding=padding.only(left=10, right=10, top=10, bottom=10),
            # bgcolor='pink',
            content=ResponsiveRow(
                controls=[
                    Column(
                        col=6,
                        expand=True,
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Text(category, size=10, color=colors.ON_PRIMARY),
                            Text(name, size=16, text_align="center", color=colors.ON_PRIMARY),
                            Text(price, size=14, color=colors.ON_PRIMARY),
                        ],
                    ),
                    Column(
                        col=6,
                        expand=True,
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.END,
                        controls=[
                            Container(
                                width=40,
                                height=40,
                                border_radius=10,
                                bgcolor=colors.PRIMARY,
                                content=Icon(name=icons.ADD, color=colors.ON_PRIMARY),
                                on_click=lambda e: self.parent_controller.add_to_cart(
                                    item_name=name, cost=price
                                ),
                            ),
                            Container(
                                width=40,
                                height=40,
                                border_radius=10,
                                bgcolor=colors.PRIMARY,
                                content=Icon(name=icons.REMOVE, color=colors.ON_PRIMARY),
                                on_click=lambda e: self.parent_controller.remove_from_cart(
                                    item_name=name, cost=price
                                ),
                            ),
                        ],
                    ),
                ]
            ),
        )
