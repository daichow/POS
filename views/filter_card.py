from flet import (
    Container,
    MainAxisAlignment,
    colors,
    UserControl,
    Text,
    alignment,
    Row,
    Text,
    alignment,
    border_radius
)


class FilterCard(UserControl):
    def __init__(self,controller):
        self.parent_controller = controller
        super().__init__()

    def items(self, count):
        items = []
        for i in range(1, count + 1):
            items.append(
                Container(
                    content=Text(value=str(i)),
                    alignment=alignment.center,
                    width=50,
                    height=30,
                    bgcolor=colors.AMBER,
                    border_radius=border_radius.all(5),
                )
            )
        return items
    
    def build(self):
        return Row(spacing=0, controls=self.items(10), alignment=MainAxisAlignment.SPACE_EVENLY)
