import flet as ft
from flet import (
    Page,
    Row,
    Container,
    margin,
    alignment,
    Card,
    Column,
    border_radius,
    padding,
    Image,
    animation,
    border,
    UserControl,
)

from flet import *
from flet.transform import Scale


class MenuItem(UserControl):
    def __init__(self, description):
        super().__init__()
        self.description = "A classic pepperoni pizza with spicy Italian sausage,\nmozzarella cheese, and our signature tomato sauce.\nEnjoy a slice or the whole pie!"

    def scaleUp(self, x):
        """scale animation for text"""
        if x.control.scale != 1.2:
            x.control.scale = 1.2
        else:
            x.control.scale = 1

        x.control.update()

    def scaleUpImage(self, x):
        """scale animation for image"""
        if x.control.scale != 1.7:
            x.control.scale = 1.7
        else:
            x.control.scale = 1.6

        x.control.update()

    def food_card(self, color_1, color_2, img_name="pizza"):
        """creates the food card and adds the image"""
        img = Container(
            on_hover=lambda x: self.scaleUpImage(x),
            scale=Scale(scale=1.6),
            animate_scale=animation.Animation(800, "bounceOut"),
            content=Image(src=f"./{img_name}.png", width=200, height=200),
        )

        return Column(horizontal_alignment="center", spacing=1, controls=[img])

    def ingredients(self, width, text):
        """takes two arguments since name length affects container width and returns a stylized text box"""
        return Container(
            on_hover=lambda x: self.scaleUp(x),
            scale=Scale(scale=1),
            animate_scale=animation.Animation(800, "bounceOut"),
            border_radius=border_radius.all(5),
            width=width,
            height=22,
            alignment=alignment.center,
            content=(Text(text, color="#f3f4f6", size=14, weight="w300")),
            gradient=LinearGradient(
                begin=alignment.bottom_left,
                end=alignment.top_right,
                colors=["#475569", "#334155"],
            ),
        )

    def nutrition_unit(self, unit):
        """create top value, grams of calories, fats, carbs, and protien"""
        return Container(
            # margin=margin.only(bottom=0),
            alignment=alignment.bottom_center,
            content=(Text(unit, color="white", size=14, weight="w400", no_wrap=True)),
        )

    def nutrition_value(self, value):
        """create top value, grams of calories, fats, carbs, and protien"""
        return Container(
            # margin=margin.only(bottom=0),
            alignment=alignment.top_center,
            content=(
                Text(value, color="#64748b", size=14, weight="w200", no_wrap=True)
            ),
        )

    def vertical_padding_container(self, value):
        return Container(padding=padding.only(top=value))

    def row_text(self, text, color, size, weight):
        return Row(controls=[Text(text, color=color, size=size, weight=weight)])

    def ingredients_row(self, ingredients_list):
        return Row(controls=[self.ingredients(70, i) for i in ingredients_list])

    def nutrition_row(self, calories="250g", fats="21g", carbs="125g", proteins="32g"):
        # create calories unit
        calories_unit = self.nutrition_unit(calories)
        calories_value = self.nutrition_value("calories")
        fat_unit = self.nutrition_unit(fats)
        fat_value = self.nutrition_value("fats")
        carbs_unit = self.nutrition_unit(carbs)
        carbs_value = self.nutrition_value("carbs")
        proteins_unit = self.nutrition_unit(proteins)
        proteins_value = self.nutrition_value("proteins")
        return Row(
            alignment="center",
            spacing=40,
            controls=[
                Column(controls=[calories_unit, calories_value]),
                Column(controls=[fat_unit, fat_value]),
                Column(controls=[carbs_unit, carbs_value]),
                Column(controls=[proteins_unit, proteins_value]),
            ],
        )

    def menu_item_price(self, price="7.99"):
        return Container(
            alignment=alignment.bottom_center,
            margin=margin.only(bottom=-5),
            padding=padding.only(right=10),
            content=(
                Text(f"${price}", color="white", size=18, weight="w400", no_wrap=True)
            ),
        )

    def add_to_cart_btn(self):
        return ElevatedButton(
            content=(Text("Add to Cart", size=18, weight="w700")),
            bgcolor="#f7ce7c",
            color="black",
            width=230,
            height=40,
        )

    def build(self):
        return Card(
            elevation=15,
            content=Container(
                alignment=alignment.center,
                width=350,
                height=650,
                content=Container(
                    padding=padding.all(20),
                    alignment=alignment.center,
                    border_radius=15,
                    gradient=LinearGradient(
                        begin=alignment.bottom_left,
                        end=alignment.top_right,
                        colors=["#1f2937", "#111827"],
                    ),
                    content=Column(
                        horizontal_alignment="center",
                        controls=[
                            self.food_card("#fffbeb", "#fef3c7"),
                            # padding before main content
                            self.vertical_padding_container(60),
                            # menu item title
                            self.row_text("Pepperoni Pizza", "#e2e8f0", 23, "w700"),
                            # create ingredients row
                            self.ingredients_row(
                                ["sauce", "pepperoni", "mozzarella", "pepper"]
                            ),
                            # more padding
                            self.vertical_padding_container(10),
                            # menu item description seperated evry 54 chars
                            self.row_text(self.description, "#64748b", 13, "w300"),
                            # more padding
                            self.vertical_padding_container(10),
                            # nutritional values row
                            self.nutrition_row(),
                            # more padding
                            self.vertical_padding_container(20),
                            # price tag and add to cart button
                            Row(
                                alignment="start",
                                controls=[
                                    Container(
                                        alignment=alignment.center,
                                        content=Row(
                                            controls=[
                                                self.menu_item_price("11.99"),
                                                self.add_to_cart_btn(),
                                            ]
                                        ),
                                    )
                                ],
                            ),
                        ],
                    ),
                ),
            ),
        )
