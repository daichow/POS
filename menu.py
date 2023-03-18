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
)

from flet import *
from flet.transform import Scale

def scaleUp(x):
    """scale animation for text"""
    if x.control.scale != 1.2:
        x.control.scale = 1.2
    else:
        x.control.scale = 1
    
    x.control.update()

def scaleUpImage(x):
    """scale animation for image"""
    if x.control.scale != 1.7:
        x.control.scale = 1.7
    else:
        x.control.scale = 1.6
    
    x.control.update()

def card(color_1, color_2):
    """creates the food card and adds the image"""
    img=Container(
        on_hover=lambda x: scaleUpImage(x),
        scale=Scale(scale=1.6),
        animate_scale=animation.Animation(800, "bounceOut"),
        content=Image(
            src=f"./pizza.png",
            width=200,
            height=200
        )
    )
    
    return Column(
        horizontal_alignment="center",
        spacing=1,
        controls=[img]
    )

def ingredients(width, text):
    """ takes two arguements since name length affects container width and returns a stylized text box"""
    return Container(
        on_hover=lambda x: scaleUp(x),
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
        )
    )

def nutrition_unit(unit):
    """create top value, grams of calories, fats, carbs, and protien"""
    return Container(
        # margin=margin.only(bottom=0),
        alignment=alignment.bottom_center,
        content=(Text(unit, color="white", size=14, weight="w400", no_wrap=True))
    )

def nutrition_value(value):
    """create top value, grams of calories, fats, carbs, and protien"""
    return Container(
        # margin=margin.only(bottom=0),
        alignment=alignment.top_center,
        content=(Text(value, color="#64748b", size=14, weight="w200", no_wrap=True))
    )

def main(page: ft.Page):
    page.title = "Menu App UI Design"
    page.window_width = 700
    page.window_height = 800
    # page.window_center() # center to screen middle

    # create a food card
    food_card = card("#fffbeb", "#fef3c7")

    # create ingredient text containers
    wagu = ingredients(55, "Wagu")
    cheese = ingredients(65, "Cheese")
    mushrooms = ingredients(90, "Mushrooms")
    onions = ingredients(65, "Onions")

    # create calories unit
    calories_unit = nutrition_unit("258")
    calories_value = nutrition_value("calories")

    fat_unit = nutrition_unit("21g")
    fat_value = nutrition_value("fats")

    carbs_unit = nutrition_unit("125g")
    carbs_value = nutrition_value("carbs")

    proteins_unit = nutrition_unit("32g")
    proteins_value = nutrition_value("proteins")

    t = Card(
        content=Container(
            alignment=alignment.center,
            width=350,
            height=650,
            # elevation=10,
            content=Container(
                content=Column(
                    horizontal_alignment="center",
                    controls=[
                        food_card,
                        # padding before main content
                        Container(padding=padding.only(top=60)), 
                        # menu item title
                        Row(controls=[Text("Pepperoni Pizza", color="#e2e8f0", size=23, weight="w700")]),
                        # create ingredients row
                        Row(controls=[wagu, cheese, mushrooms, onions]),
                        # more padding
                        Container(padding=padding.only(top=10)),
                        # menu item description seperated evry 54 chars
                        Row(
                            controls=[Text("A classic pepperoni pizza with spicy Italian sausage,\nmozzarella cheese, and our signature tomato sauce.\nEnjoy a slice or the whole pie!",
                            color="#64748b",
                            size=13, 
                            weight="w300",
                            no_wrap=True)]
                        ),
                        # more padding
                        Container(padding=padding.only(top=10)),
                        # nutritional values row
                        Row(alignment="center", spacing=40, controls=[
                            Column(controls=[calories_unit, calories_value]),
                            Column(controls=[fat_unit, fat_value]),
                            Column(controls=[carbs_unit, carbs_value]),
                            Column(controls=[proteins_unit, proteins_value]),
                        ]),
                        # more padding
                        Container(padding=padding.only(top=20)),
                        # price tag and add to cart button
                        Row(alignment="start", controls=[
                            Container(alignment=alignment.center, content=Row(
                                controls=[
                                    Container(
                                        alignment=alignment.bottom_center,
                                        margin=margin.only(bottom=-5),
                                        padding=padding.only(right=10),
                                        content=(Text("$7.99", color="white", size=18, weight="w400", no_wrap=True))
                                    ),
                                    ElevatedButton(
                                        content=(Text("Add", size=18, weight="w700")),
                                        bgcolor="#f7ce7c",
                                        color="black",
                                        width=230,
                                        height=40,
                                    )
                                ])
                            )
                        ]),

                    ]
                ),
                padding=padding.all(20),
                alignment=alignment.center,
                border_radius=border_radius.all(12),
                gradient=LinearGradient(
                    begin=alignment.bottom_left,
                    end=alignment.top_right,
                    colors=["#1f2937", "#111827"],
                ),
            )
        )
    )

    # create a container for background gradient effect
    c = Container(
        Column(
            alignment="center",
            controls=[t]
        ),
        gradient=LinearGradient(
            begin=alignment.bottom_left,
            end=alignment.top_right,
            colors=["#1e293b", "#475569"]
        ),
        alignment=alignment.center,
        width=700,
        height=800,
        margin=margin.all(-10)
    )
    page.add(c)
    page.update()

    # audio1 = ft.Audio(
    #     src="https://luan.xyz/files/audio/ambient_c_motion.mp3", autoplay=True
    # )
    # page.overlay.append(audio1)
    # page.add(
    #     ft.Text("This is an app with background audio."),
    #     ft.ElevatedButton("Stop playing", on_click=lambda _: audio1.pause()),
    # )

ft.app(target=main, assets_dir="assets")