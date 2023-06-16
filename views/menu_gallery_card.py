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
)


class CardGenerator(UserControl):
    # We'll need to be passing in arguments here which will be called from the data module in data.py
    def __init__(
        self,
        # The CardGnerator class will take in several arguments with their data type, so ex: colors will be a list
        # when we call this class in the main.py file, we can set each argument to a specific value in the dictioanry
        colors: list,
        title: str,
    ):
        self.colors = colors
        self.title = title

        super().__init__()

    def show_price(self, e):
        if e.data == "true":
            self.animated_text.offset = transform.Offset(0, 0)
            self.animated_text.opacity = 1
            self.animated_text.update()
        else:
            self.animated_text.offset = transform.Offset(0.25, 0)
            self.animated_text.opacity = 0
            self.animated_text.update()

    def build(self):
        # food card
        # self.food_card = Container(
        #     # offset=transform.Offset(0, 0),
        #     # animate_offset=animation.Animation(900),
        #     content=Card(
        #         width=100,
        #         height=100,
        #         elevation=20,
        #         bgcolor="white",
        #         content=Container(
        #             width=56,
        #             height=56,
        #             border_radius=20
        #         ),
        #     ),
        # )

        # animated text
        # self.animated_text = Text(
        #     self.price,
        #     size=18,
        #     weight="bold",
        #     offset=transform.Offset(0.35, 0),
        #     animate_offset=animation.Animation(
        #         duration=900, curve="decelerate"),
        #     animate_opacity=300,
        #     opacity=0,
        # )
        # main continer
        self.main_card = Container(
            gradient=RadialGradient(
                center=Alignment(0.8, 0.8),
                radius=1.4,
                # the self.colors in this case is the list of colors from the pyhton dictioanry
                colors=self.colors,
            ),
            # width=200,
            # height=300,
            border_radius=10,
            alignment=alignment.bottom_center,
            content=Column(
                alignment="start",
                horizontal_alignment="center",
                controls=[
                    Card(
                        width=300,
                        height=120,
                        opacity=0.5,
                    )
                ],
            ),
        )

        return self.main_card
