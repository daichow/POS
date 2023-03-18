from flet import (
    Container,
    UserControl,
    RadialGradient,
    Alignment,
    alignment,
    Row,
    border_radius,
    padding,
    Column,
    Text,
    Card,
    animation,
    transform,
    MainAxisAlignment
)
from ui.cart_item import CartItem


class Cart(UserControl):
    def __init__(
            self,
            model,
            controller,
            window_width: int,
            window_height: int,
            title: str = None,):
        self.parent_controller = controller
        self.model = model
        self.title = title
        self.window_width = window_width
        self.window_height = window_height

        super().__init__()

    def build(self):
        # return a column of cards
        return Container(
            padding=10,
            border_radius=10,
            alignment=alignment.center,
            content=Column(
                ref=self.model.cart_list_view,
            ),
            width=self.window_width * 0.3,
            height=self.window_height,
            bgcolor='black'
        )
