import flet as ft


class CartItem(ft.UserControl):
    def __init__(self, number, item_name, quantity, cost, controller):
        self.parent_controller = controller
        self.number = number
        self.item_name = item_name
        self.quantity = quantity
        self.cost = cost
        super().__init__()

    def build(self):
        return ft.Container(
            expand=True,
            height=50,
            bgcolor='white10',
            border_radius=11,
            padding=ft.padding.only(left=10, right=10, top=10, bottom=10),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=20,
                        height=20,
                        bgcolor='white',
                        shape=ft.BoxShape.CIRCLE,
                        alignment=ft.alignment.center,
                        content=ft.Text(
                            self.number, size=11, weight='bold', color='black')
                    ),

                    ft.Text(self.item_name, size=12),
                    ft.Text(self.quantity, size=10, color='grey'),
                    ft.Text(self.cost, size=14),
                    ft.Container(
                        width=30,
                        height=30,
                        bgcolor='transparent',
                        # shape=ft.BoxShape.CIRCLE,
                        alignment=ft.alignment.center,
                        content=ft.Icon(
                            name=ft.icons.DELETE_ROUNDED, color='red'),
                        on_click=lambda e: self.parent_controller.delete_from_cart(
                            self.number)
                    )
                ])
        )
