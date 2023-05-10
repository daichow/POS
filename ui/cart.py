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
    MainAxisAlignment,
    CrossAxisAlignment,
    Divider,
    icons,
    colors,
    Icon,
    ElevatedButton,
    RoundedRectangleBorder,
    ButtonStyle,
    TextField,
)
from flet.types import TextAlign
from ui.cart_item import CartItem


class Cart(UserControl):
    def __init__(
        self,
        model,
        controller,
        window_width: int,
        window_height: int,
        title: str = None,
    ):
        self.parent_controller = controller
        self.model = model
        self.title = title
        self.window_width = window_width
        self.window_height = window_height

        super().__init__()

    def build(self):
        # return a column of cards
        return Column(
            [
                Container(
                    padding=10,
                    border_radius=10,
                    alignment=alignment.top_center,
                    content=Column(
                        ref=self.model.cart_list_view,
                        scroll="always",
                        auto_scroll=True
                        # height=self.window_height*0.5
                    ),
                    width=self.window_width * 0.3,
                    height=self.window_height * 0.5,
                    bgcolor="black",
                ),
                Container(
                    padding=30,
                    border_radius=10,
                    alignment=alignment.top_center,
                    content=Column(
                        alignment=MainAxisAlignment.START,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Row(
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    Text("Subtotal"),
                                    Text(ref=self.model.subtotal),
                                ],
                            ),
                            Row(
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    Text("Discount"),
                                    TextField(
                                        ref=self.model.discount,
                                        border_color="transparent",
                                        text_size=14,
                                        prefix_text="-$",
                                        content_padding=20,
                                        cursor_color="white",
                                        cursor_width=1,
                                        text_align=TextAlign.RIGHT,
                                        width=200,
                                        height=50,
                                        hint_text="0.00",
                                        on_change=lambda e: self.parent_controller.calculate_totals(),
                                    ),
                                ],
                            ),
                            Row(
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[Text("Tax 13%"), Text(ref=self.model.tax)],
                            ),
                            Divider(height=5, color="white"),
                            Row(
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[Text("Total"), Text(ref=self.model.total)],
                            ),
                            Divider(height=10, color="white"),
                            # Text("Payment Method"),
                            Row(
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    Container(
                                        ref=self.model.cash_button,
                                        width=100,
                                        height=50,
                                        border_radius=10,
                                        bgcolor="white",
                                        content=Icon(
                                            name=icons.ATTACH_MONEY_ROUNDED,
                                            color=colors.GREEN,
                                        ),
                                        on_click=lambda e: self.parent_controller.pay_with_cash(
                                            self.model.total.current.value
                                        ),
                                    ),
                                    Container(
                                        ref=self.model.card_button,
                                        width=100,
                                        height=50,
                                        border_radius=10,
                                        bgcolor="white",
                                        content=Icon(
                                            name=icons.CREDIT_CARD, color=colors.BLACK
                                        ),
                                        on_click=lambda e: self.parent_controller.pay_with_card(),
                                    ),
                                ],
                            ),
                            ElevatedButton(
                                "Place Order",
                                color="black",
                                bgcolor="white",
                                width=self.window_width * 0.2,
                                height=50,
                                style=ButtonStyle(
                                    shape=RoundedRectangleBorder(radius=10)
                                ),
                                on_click=lambda e: self.parent_controller.place_order(),
                            ),
                        ],
                    ),
                    width=self.window_width * 0.3,
                    height=self.window_height * 0.5,
                    bgcolor="black",
                ),
            ]
        )
