from flet_mvc import FletController, alert
from flet import colors

# from escpos.printer import Usb
import subprocess
from subprocess import call
import json

# from api import luxmo_api
import flet as ft
from ui.item import Item
from ui.cart_item import CartItem

# Controller
from rapidfuzz import process, fuzz
import pprint

from datetime import datetime


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
                update_msg = (
                    f"{diff} new invoices were found."
                    if diff != 1
                    else "A new invoice was found."
                )
            else:
                update_msg = (
                    f"{diff * -1} invoices have been removed."
                    if diff != -1
                    else "One invoice has been removed"
                )

            self.alert(f"The view has been reloaded. {update_msg}", alert.INFO)

        self.update()

    def create_labels(self, e):
        # Error handling
        if self.model.checked_items() == 0:
            self.alert(
                "! [ERROR] No invoice was selected. Please select an invoice and try again.",
                alert.ADVICE,
            )
        elif self.model.utility() <= 0 and type(self.model.utility()) != str:
            self.alert(
                "! [ERROR] - Utility percentage should be greater than 0.0%",
                alert.ADVICE,
            )

        # Creating labels
        else:
            try:
                # Main
                # luxmo_api(self.model.utility(), self.model.files())

                # Reload view
                self.reload_app(show_alert=False)

                # Succeed msg
                self.alert(
                    "The labels have been created. The selected invoices\nhave been moved to the 'labeled_invoices' folder",
                    alert.SUCCESS,
                )

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
        res = process.extract(e.control.value, choices, limit=len(self.model.menu()))

        # print(res)

        self.model.menu.set_value([result[0] for result in res if result[1] > 40])

        if not self.model.menu():
            self.model.menu.reset()

        # print(self.model.menu(), "\n\n\n\n")

        result.value = f"search results: {len(self.model.menu())}"

        self.model.menu_list_view.current.controls = self.items(self.model.menu(), self)

        self.update()

    def on_item_click(self, e):
        print(e.control.content.value)
        self.update()

    def items(self, item_list, parent_controller):
        items = []
        for i in item_list:
            items.append(Item(str(i), parent_controller))
        return items

    def add_to_cart(self, item_name, cost):
        self.reorder_cart()

        # quantity = 0
        found = False

        for i, cart_item in enumerate(self.model.cart_list_view.current.controls):
            if (
                cart_item.item_name == item_name
                and cart_item.item_name not in self.model.toppings
                and cart_item.item_name not in self.model.pizzas
            ):
                found = True
                quantity = int(cart_item.quantity[1:]) + 1
                self.model.cart_list_view.current.controls[i] = CartItem(
                    cart_item.number, item_name, f"x{quantity}", cost, controller=self
                )

        if not found:
            num = str(len(self.model.cart_list_view.current.controls))
            quantity = 1
            self.model.cart_list_view.current.controls.append(
                CartItem(num, item_name, f"x{quantity}", cost, controller=self)
            )

        print("added to cart ", item_name)
        self.calculate_totals()
        self.update()

    def remove_from_cart(self, item_name, cost):
        self.reorder_cart()

        for i, cart_item in enumerate(self.model.cart_list_view.current.controls):
            if (
                cart_item.item_name == item_name
                and cart_item.item_name not in self.model.toppings
                and cart_item.item_name not in self.model.pizzas
            ):
                quantity = int(cart_item.quantity[1:]) - 1
                if quantity == 0:
                    del self.model.cart_list_view.current.controls[i]
                else:
                    self.model.cart_list_view.current.controls[i] = CartItem(
                        cart_item.number,
                        item_name,
                        f"x{quantity}",
                        cost,
                        controller=self,
                    )

        print("removed from cart ", item_name)
        self.calculate_totals()
        self.update()

    def delete_from_cart(self, number):
        print("deleting ", number)
        del self.model.cart_list_view.current.controls[int(number)]
        self.calculate_totals()
        self.reorder_cart()

    def reorder_cart(self):
        reordered_list = []
        for index, cart_item in enumerate(self.model.cart_list_view.current.controls):
            reordered_list.append(
                CartItem(
                    index,
                    cart_item.item_name,
                    cart_item.quantity,
                    cart_item.cost,
                    controller=self,
                )
            )
        self.model.cart_list_view.current.controls = reordered_list

    def calculate_totals(self):
        subtotal = 0
        tax = 0
        total = 0
        for cart_item in self.model.cart_list_view.current.controls:
            subtotal += float(cart_item.cost[1:]) * float(cart_item.quantity[1:])

        subtotal = "{:.2f}".format(round(subtotal, 2))

        if self.model.discount.current.value != "":
            discount = float(self.model.discount.current.value)
        else:
            discount = float("0.00")

        subtotal_w_discount = float(subtotal) - discount
        total = "{:.2f}".format(round(float(subtotal_w_discount) * 1.13, 2))
        tax = "{:.2f}".format(round(float(total) - float(subtotal_w_discount), 2))

        self.model.subtotal.current.value = f"${subtotal}"
        self.model.tax.current.value = f"${tax}"
        self.model.total.current.value = f"${total}"

    def calculate_change(self, total_price, amount_given):
        print(amount_given)
        # Calculate change in cents
        change = round((amount_given - total_price) * 100)

        # Define available denominations of bills and coins
        denominations = {
            "100": 100.00,
            "50": 50.00,
            "20": 20.00,
            "10": 10.00,
            "5": 5.00,
            "2": 2.00,
            "1": 1.00,
            "25c": 0.25,
            "10c": 0.10,
            "5c": 0.05,
        }

        # Initialize empty dictionary to store number of each denomination needed for change
        num_denominations = {}

        # Loop through available denominations and calculate number of each needed for change
        for denomination, value in denominations.items():
            if change >= int(value * 100):
                num_denominations[denomination] = int(change // int(value * 100))
                change %= int(value * 100)

        print(num_denominations)
        images = []
        # money = ["5", "10", "20", "50", "100", "5c", "10c", "25c", "1", "2"]
        for bill, num in num_denominations.items():
            images.append(
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    controls=[
                        ft.Image(
                            src=f"{bill}.png",
                            fit=ft.ImageFit.SCALE_DOWN,
                            width=200,
                        ),
                        ft.Text(f"x {num}", size=26, color="white", weight="bold"),
                    ],
                )
            )
        self.model.images = images
        # print(self.model.images)
        self.model.change_column.current.controls = [
            self.model.change_column.current.controls[0]
        ]
        self.model.change_column.current.controls.extend(self.model.images)
        # print(self.model.change_column.current.controls)
        self.update()

    def pay_with_cash(self, total_price):
        self.model.card_button.current.content.color = colors.BLACK
        self.model.cash_button.current.content.color = colors.GREEN

        # alert = self.alert()

        def close_dlg(e):
            dlg_modal.open = False
            self.update()

        def open_register(controller):
            controller.alert(
                "Opened the Register. Please return the appropriate change.", "success"
            )

        money_given_tx_field = ft.TextField(
            label="Enter the Cash Given by the Customer",
            on_change=lambda e: self.calculate_change(
                float(total_price[1:]), float(e.control.value)
            ),
        )
        alert = ft.Container(
            content=ft.Column(ref=self.model.change_column, scroll=ft.ScrollMode.AUTO),
            width=300,
            height=300,
        )
        self.model.change_column.current.controls.append(money_given_tx_field)
        dlg_modal = ft.AlertDialog(
            modal=True,
            content=alert,
            actions=[
                ft.ElevatedButton(
                    "Open Register",
                    color="white",
                    bgcolor="green",
                    on_click=lambda e: open_register(self),
                ),
                ft.ElevatedButton(
                    "Exit", color="white", bgcolor="red", on_click=close_dlg
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.dialog = dlg_modal
        dlg_modal.open = True
        self.update()

    def pay_with_card(self):
        self.model.card_button.current.content.color = colors.GREEN
        self.model.cash_button.current.content.color = colors.BLACK

    def get_current_formatted_date(self):
        date_format = "%d-%b-%Y %I:%M:%S%p"
        return datetime.now().strftime(date_format)

    def place_order(self):
        order_list = []
        temp_toppings = []

        payment_type = ""
        if self.model.card_button.current.content.color == colors.GREEN:
            payment_type = "card"
        else:
            payment_type = "cash"

        current_cart = self.model.cart_list_view.current.controls

        for item in current_cart:
            if item.item_name not in self.model.toppings:  # if it isn't a topping
                order_list.append(f"{item.quantity[1:]} x {item.item_name}")
                if len(temp_toppings) != 0:
                    order_list[-2] = order_list[-2] + f" ({', '.join(temp_toppings)})"
                    temp_toppings = []
            elif item.item_name in self.model.toppings:
                temp_toppings.append(item.item_name)

        if len(temp_toppings) != 0:
            order_list[-1] = order_list[-1] + f" ({', '.join(temp_toppings)})"

        order = f"{self.get_current_formatted_date()};{', '.join(order_list)};{payment_type};{self.model.total.current.value}"
        print(order.split(";"))
        self.alert("Order Placed and Recorded. Printing Reciept.", alert.SUCCESS)
        self.model.client.open("University Pizza").worksheet("Sales").append_row(
            order.split(";")
        )

        order = order.split(";")

        datetime_list = [
            f"Date: {order[0].split(' ')[0]}\n",
            f"Time: {order[0].split(' ')[1]}\n",
            "\n",
        ]
        item_list = []
        spacing = 40
        for item in current_cart:
            item_list.append(
                "{:<{}}{}".format(
                    f"{item.quantity[1:]} x {item.item_name}",
                    spacing,
                    f"{item.cost}\n",
                )
            )
        item_list.append("\n")

        spacing = 30
        cost_list = [
            "{:<{}}{}".format("Method:", spacing, f"{order[2]}\n"),
            "{:<{}}{}".format(
                "Subtotal:", spacing, f"{self.model.subtotal.current.value}\n"
            ),
            "{:<{}}{}".format(
                "Discount", spacing, f"-${self.model.discount.current.value}\n"
            ),
            "{:<{}}{}".format("Tax 13%:", spacing, f"{self.model.tax.current.value}\n"),
            "{:<{}}{}".format("Total:", spacing, f"{self.model.total.current.value}\n"),
            "\n",
        ]

        json_data = {
            "cash": order[2] == "cash",
            "datetime": datetime_list,
            "item": item_list,
            "cost": cost_list,
        }

        json_str = json.dumps(json_data)

        # Password to use for sudo
        password = "ASDF ;lkj"

        # List of arguments to pass to the second script
        cmd = ["sudo", "python3", "./printer.py"]

        # Loop over each list of strings in the data list and append it to the arguments
        # for lst in data:
        #     args.extend(lst)

        # Run the second script with sudo privileges and pass the password to it
        # result = subprocess.run(cmd, input=json_str.encode(), capture_output=True)
        # print(result.stdout.decode())
        call('echo {} | sudo -S {}'.format(password, cmd), shell=True)
        # output, error = process.communicate(password.encode())
