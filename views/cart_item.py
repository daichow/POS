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
            bgcolor=ft.colors.PRIMARY,
            border_radius=11,
            padding=ft.padding.only(left=10, right=10, top=10, bottom=10),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=20,
                        height=20,
                        bgcolor=ft.colors.ON_PRIMARY,
                        shape=ft.BoxShape.CIRCLE,
                        alignment=ft.alignment.center,
                        content=ft.Text(
                            self.number, size=11, weight='bold', color=ft.colors.PRIMARY)
                    ),

                    ft.Text(self.item_name[:20], size=12, color=ft.colors.ON_PRIMARY,),
                    ft.Text(self.quantity, size=10, color=ft.colors.ON_PRIMARY,),
                    ft.Text(self.cost, size=14, color=ft.colors.ON_PRIMARY,),
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
