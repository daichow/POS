from flet_mvc import FletView
from flet import *
from views.navbar import NavBar
from views.cart import Cart
from views.search import DropdownSearchBar
from views.item_list import ItemList
from views.filter_card import FilterCard

# View


class MainView(FletView):
    def __init__(self, controller, model):
        WIDTH = 1000
        HEIGHT = 700
        self.item_list = ItemList(model, controller)
        self.cart = Cart(model, controller, WIDTH, HEIGHT)
        view = [
            Container(
                bgcolor=colors.SURFACE,
                content=Row(
                    alignment=MainAxisAlignment.START,
                    controls=[
                        # NavBar(controller, h=HEIGHT),
                        Container(
                            content=Column(
                                alignment=MainAxisAlignment.START,
                                controls=[
                                    # This contains all of the UserControls in the middle
                                    DropdownSearchBar(controller),
                                    FilterCard(controller),
                                    self.item_list,
                                ],
                                height=HEIGHT,
                            ),
                            expand=True,
                        ),
                        self.cart,
                    ],
                ),
            )
        ]

        super().__init__(model, view, controller)
