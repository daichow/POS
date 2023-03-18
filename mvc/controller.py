from flet_mvc import FletController, alert
# from api import luxmo_api
import flet as ft
from ui.item import Item
from ui.cart_item import CartItem
# Controller
from rapidfuzz import process, fuzz
import pprint


class Controller(FletController):

    def on_icon_click(self, e):
        """
        NOTE: This is the method that we want to be called
        whenever we click a button of the ModernNavBar User Control.

        But how is it called?
        Take a look at /user_controls/navbar.py > on_icon_click
        """
        value = e.control.content.controls[1].value
        self.model.text.current.value = f"You clicked: {value}"
        # self.alert("clicked a tab", alert.INFO)
        self.update()

    def item_selected(self, e=None, invoice_number=None, file=None):
        if e.data == "true":
            self.model.checked_items.set_value(self.model.checked_items() + 1)
            self.model.files().append(file)
        else:
            self.model.checked_items.set_value(self.model.checked_items() - 1)
            self.model.files().remove(file)

    def reload_app(self, e=None, show_alert=True):
        last_one = self.model.n_invoices()
        self.model.n_invoices.reset()
        self.model.files.reset()
        self.model.info.current.value = self.model.found_invoices()
        self.model.create_checkboxes()
        self.model.checked_items.reset()

        if show_alert:
            # Update Msg
            diff = self.model.n_invoices() - last_one
            if diff == 0:
                update_msg = "No Invoice Found."
            elif diff > 0:
                update_msg = f"{diff} new invoices were found." if diff != 1 else "A new invoice was found."
            else:
                update_msg = f"{diff * -1} invoices have been removed." if diff != - \
                    1 else "One invoice has been removed"

            self.alert(f"The view has been reloaded. {update_msg}", alert.INFO)

        self.update()

    def create_labels(self, e):
        # Error handling
        if self.model.checked_items() == 0:
            self.alert(
                "! [ERROR] No invoice was selected. Please select an invoice and try again.", alert.ADVICE)
        elif self.model.utility() <= 0 and type(self.model.utility()) != str:
            self.alert(
                "! [ERROR] - Utility percentage should be greater than 0.0%", alert.ADVICE)

        # Creating labels
        else:
            try:
                # Main
                # luxmo_api(self.model.utility(), self.model.files())

                # Reload view
                self.reload_app(show_alert=False)

                # Succeed msg
                self.alert(
                    "The labels have been created. The selected invoices\nhave been moved to the 'labeled_invoices' folder", alert.SUCCESS)

            except Exception as e:
                self.alert(f"[ERROR] Contact support -- Error found: {e}")

    def check_digits_only(self, e):
        try:
            self.model.utility.set_value(float(e.data))
            e.control.error_text = None
        except ValueError:
            self.model.utility.reset()
            e.control.error_text = "[ERROR] Only digits are allowed"

        self.update()

    def on_keyboard(self, e: ft.KeyboardEvent):
        if e.key == "D" and e.alt and e.shift:
            self.page.show_semantics_debugger = not self.page.show_semantics_debugger
            self.page.update()

    def filter_search_items(self, e, result):
        # print(e.control.value, len(self.model.menu()))
        self.model.menu.reset()
        # print("original length", self.model.menu())
        choices = self.model.menu()
        res = process.extract(
            e.control.value, choices, limit=len(self.model.menu()))

        # print(res)

        self.model.menu.set_value([result[0]
                                  for result in res if result[1] > 40])

        if not self.model.menu():
            self.model.menu.reset()

        print(self.model.menu(), "\n\n\n\n")

        result.value = f"search results: {len(self.model.menu())}"

        self.model.menu_list_view.current.controls = self.items(
            self.model.menu(), self)

        self.update()

    def on_item_click(self, e):
        print(e.control.content.value)
        self.update()

    def items(self, item_list, parent_controller):
        items = []
        for i in item_list:
            items.append(
                Item(str(i), parent_controller)
            )
        return items

    def add_to_cart(self, item_name, cost):
        num = str(len(self.model.cart_list_view.current.controls))
        # quantity = 0
        found = False

        for i, cart_item in enumerate(self.model.cart_list_view.current.controls):
            if cart_item.item_name == item_name:
                found = True
                print("FOUND")
                quantity = quantity + 1
                self.model.cart_list_view.current.controls[i] = CartItem(
                    num, item_name, quantity, cost, controller=self)

        if not found:
            quantity = 0
            self.model.cart_list_view.current.controls.append(CartItem(
                num, item_name, quantity, cost, controller=self))

        print("added to cart ", item_name)
        self.update()

    def delete_from_cart(self, number):
        print("deleting ", number)
        del self.model.cart_list_view.current.controls[int(number)]

        reordered_list = []
        for index, cart_item in enumerate(self.model.cart_list_view.current.controls):
            reordered_list.append(CartItem(index, cart_item.item_name, cart_item.quantity,
                                           cart_item.cost, controller=self))
        self.model.cart_list_view.current.controls = reordered_list
