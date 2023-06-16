from flet_mvc import FletController, alert
from flet import colors

import subprocess
from subprocess import call
import json

# from api import luxmo_api
import flet as ft
from views.item import Item
from views.cart_item import CartItem

# Controller
from rapidfuzz import process, fuzz
import pprint

from datetime import datetime
from escpos.printer import Usb


class Controller(FletController):
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

        change = round((amount_given - total_price) * 100)
        num_denominations = {}

        for denomination, value in denominations.items():
            denomination_value = int(value * 100)
            if change >= denomination_value:
                num_denominations[denomination] = change // denomination_value
                change %= denomination_value

        images = []
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
        self.model.change_column.current.controls = [
            self.model.change_column.current.controls[0]
        ]
        self.model.change_column.current.controls.extend(self.model.images)
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
        payment_type = self.get_payment_type()

        current_cart = self.model.cart_list_view.current.controls

        order_list = self.create_order_list(current_cart, temp_toppings)

        order = self.create_order_string(order_list, payment_type)
        self.process_order(order)
        self.print_receipt(order, current_cart)

    def get_payment_type(self):
        if self.model.card_button.current.content.color == colors.GREEN:
            return "card"
        else:
            return "cash"

    def create_order_list(self, current_cart, temp_toppings):
        order_list = []
        for item in current_cart:
            if item.item_name not in self.model.toppings:
                order_list.append(f"{item.quantity[1:]} x {item.item_name}")
                if len(temp_toppings) != 0:
                    order_list[-2] = order_list[-2] + f" ({', '.join(temp_toppings)})"
                    temp_toppings = []
            elif item.item_name in self.model.toppings:
                temp_toppings.append(item.item_name)
        if len(temp_toppings) != 0:
            order_list[-1] = order_list[-1] + f" ({', '.join(temp_toppings)})"
        return order_list

    def create_order_string(self, order_list, payment_type):
        order = f"{self.get_current_formatted_date()};{', '.join(order_list)};{payment_type};{self.model.total.current.value}"
        return order

    def process_order(self, order):
        order = order.split(";")
        self.alert("Order Placed and Recorded. Printing Receipt.", alert.SUCCESS)
        self.model.client.open("University Pizza").worksheet("Sales").append_row(order)

    def print_receipt(self, order, current_cart):
        print(order)
        order_date, order_name, payment_method, order_cost = order.split(";")

        datetime_list = [
            f"Date: {order_date.split(' ')[0]}\n",
            f"Time: {order_date.split(' ')[1]}\n",
            "\n",
        ]

        item_list = []
        spacing = 40
        for item in current_cart:
            item_list.append(
                "{:<{}}{}".format(
                    f"{item.quantity[1:]} x {item.item_name}", spacing, f"{item.cost}\n"
                )
            )
        item_list.append("\n")

        spacing = 30
        cost_list = [
            "{:<{}}{}".format("Method:", spacing, f"{payment_method}\n"),
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
            "cash": payment_method == "cash",
            "datetime": datetime_list,
            "item": item_list,
            "cost": cost_list,
        }

        # Print the lists of strings
        # print(json_data)

        # Device Information
        # - Vendor ID: 1fc9
        # - Product ID: 2016
        # - Bus and Device ID: Bus 003 Device 002: ID 1fc9:2016 NXP Semiconductors Printer-80

        # Check Device Interface
        # - Run: lsusb -vvv -d 1fc9:2016 | grep iInterface
        # - Output: Couldn't open device, some information will be missing
        # - Output: iInterface 0

        # Check Endpoint Address
        # - Run: lsusb -vvv -d 1fc9:2016 | grep bEndpointAddress | grep OUT
        # - Output: Couldn't open device, some information will be missing
        # - Output: bEndpointAddress 0x01 EP 1 OUT

        # If you encounter permissions error, perform the following steps:
        # - Run: sudo sh -c 'echo "SUBSYSTEMS==\"usb\", ATTRS{idVendor}==\"1fc9\", ATTRS{idProduct}==\"2016\", GROUP=\"users\", MODE=\"0666\"" >> /etc/udev/rules.d/80-myusb.rules'

        # Refresh UDEV Rules
        # - Run: sudo udevadm control --reload-rules && sudo udevadm trigger

        p = Usb(0x1FC9, 0x2016)

        paper_status = p.paper_status()
        debug_messages = {
            2: "Paper is adequate.",
            1: "Paper ending.",
            0: "No paper.",
        }
        print(debug_messages.get(paper_status, "Unknown paper status."))

        # if json_data["cash"]:
        #     p.cashdraw(2)

        # HEADER
        p.set(align="center", font="a", custom_size=True, width=3, height=3, bold=True)
        p.text("UNIVERSITY PIZZA\n\n")
        p.set(align="center", font="b", custom_size=True, width=2, height=1)
        p.text("1457 University Ave West\n")
        p.text("Windsor, Ontario, N9B1B8\n")
        p.text("226-782-9600\n")
        p.text("\n")

        # DATETIME
        p.set(align="right", font="a", custom_size=True, width=1, height=1, bold=False)
        for d in json_data["datetime"]:
            p.text(d)

        # PRINT ITEMS
        p.set(align="center", font="a", custom_size=True, width=1, height=1, bold=False)
        for d in json_data["item"]:
            p.text(d)

        ## PRINT TOTALS
        p.set(align="center", font="a", custom_size=True, width=1, height=1, bold=True)
        for d in json_data["cost"]:
            p.text(d)

        #  CLOSING
        p.set(align="center", font="a", custom_size=True, width=1, height=1, bold=False)
        p.text("Thank you for your business!\n")
        p.cut()
        p.close()
