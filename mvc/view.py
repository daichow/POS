from flet_mvc import FletView
from flet import *
from ui.navbar import NavBar
from ui.cart import Cart
from ui.search import DropdownSearchBar
from ui.item_list import ItemList
# View


class MainView(FletView):

    def __init__(self, controller, model):
        WIDTH = 1000
        HEIGHT = 700
        self.item_list = ItemList(model, controller)
        self.cart = Cart(model, controller, WIDTH, HEIGHT)
        content = [
            Row(
                alignment=MainAxisAlignment.START,
                controls=[
                    # NavBar(controller, h=HEIGHT),
                    Container(content=Column(
                        alignment=MainAxisAlignment.START,
                        controls=[
                            # This contains all of the UserControls in the middle
                            # Divider(height=5, color="transparent"),
                            DropdownSearchBar(controller),
                            self.item_list
                        ], height=HEIGHT), expand=True),

                    self.cart
                ]
            )
        ]

        super().__init__(model, content, controller)
