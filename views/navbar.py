""" Flet UI Siderbar """

# modules
import flet as ft
from functools import partial
import time


# Sidebar Class
class NavBar(ft.UserControl):
    def __init__(self, parent_controller, h):
        self.parent_controller = parent_controller
        self.h = h
        super().__init__()

    def on_icon_click(self, e):
        """
        NOTE: See how I call the method of the app's controller here.
        This is just one option, alternatively you can just manage everything
        here in the User Control, see the function commented below:
        """
        self.parent_controller.on_icon_click(e)

    # def on_icon_click(self, e):
    #     value = e.control.content.controls[1].value
    #     self.parent_model.text.current.value = f"You clicked: {value}"
    #     self.parent_controller.alert("clicked a tab", "info")
    #     self.parent_controller.update()

    def AnimateSidebar(self, e):
        # Before it used to be outside the UserControl as: page.controls[0]
        # but we can have the same result with: self

        # We access the container on the row
        if self.controls[0].width != 62:
            for item in (
                self.controls[0]
                .content.controls[0]
                .content.controls[1]
                .controls[:]
            ):
                item.opacity = 0
                item.update()
            # opacity in icons
            for item in self.controls[0].content.controls[3:]:
                if isinstance(item, ft.Container):
                    item.content.controls[1].opacity = 0
                    item.content.update()
            time.sleep(0.2)
            self.controls[0].width = 62
            self.controls[0].update()

        else:
            self.controls[0].width = 200
            self.controls[0].update()

            time.sleep(0.2)

            for item in (
                self.controls[0]
                .content.controls[0]
                .content.controls[1]
                .controls[:]
            ):
                item.opacity = 1
                item.update()

            # opacity in icons
            for item in self.controls[0].content.controls[3:]:
                if isinstance(item, ft.Container):
                    item.content.controls[1].opacity = 1
                    item.content.update()

    # To highlight all the row when hovering the icons:

    def Highlight(self, e):
        if e.data == 'true':
            e.control.bgcolor = 'white10'
            e.control.update()
            e.control.content.controls[0].icon_color = 'white'
            e.control.content.controls[1].icon_color = 'white'
            e.control.content.update()

        else:
            e.control.bgcolor = None
            e.control.update()
            e.control.content.controls[0].icon_color = 'white54'
            e.control.content.controls[1].icon_color = 'white54'
            e.control.content.update()

    def UserData(self, initials: str, name: str, description: str):
        # idk
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=42,
                        height=42,
                        bgcolor="bluegrey500",
                        alignment=ft.alignment.center,
                        border_radius=8,
                        content=ft.Text(
                            value=initials,
                            size=20,
                            weight="bold"
                        )
                    ),
                    ft.Column(
                        spacing=1,
                        alignment="center",
                        controls=[
                            ft.Text(
                                value=name,
                                size=11,
                                weight="bold",
                                opacity=1,
                                animate_opacity=200,
                            ),
                            ft.Text(
                                value=description,
                                size=9,
                                weight="w400",
                                color='white54',
                                opacity=1,
                                animate_opacity=200,
                            )
                        ]
                    )
                ]
            )
        )

    # now for the main sidebar row and icons
    def ContainedIcons(self, icon_name: str, text: str):
        return ft.Container(
            width=180,
            height=45,
            border_radius=10,
            on_hover=lambda e: self.Highlight(e),
            on_click=self.on_icon_click,
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=icon_name,
                        icon_size=18,
                        icon_color='white54',
                        style=ft.ButtonStyle(
                            shape={
                                "": ft.RoundedRectangleBorder(radius=7)
                            },
                            overlay_color={
                                "": "transparent"
                            }
                        ),

                    ),
                    ft.Text(
                        value=text,
                        color="white54",
                        size=11,
                        opacity=1,
                        animate_opacity=200,

                    )
                ]
            )
        )

    def build(self):
        return ft.Container(
            width=200,
            height=self.h,
            # height=675,
            # expand=True,
            bgcolor='black',
            border_radius=10,
            animate=ft.animation.Animation(500, 'decelerate'),
            padding=10,
            alignment=ft.alignment.center,
            content=ft.Column(
                # alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment="center",
                controls=[
                    self.UserData("UU", "Use UserControl",
                                  "Inside other apps"),
                    ft.Divider(
                        height=5,
                        color="transparent"
                    ),

                    ft.Container(
                        width=24,
                        height=24,
                        bgcolor="bluegrey800",
                        border_radius=8,
                        on_click=partial(self.AnimateSidebar)
                    ),

                    ft.Divider(
                        height=5,
                        color="transparent"
                    ),

                    # Sidebar icons
                    self.ContainedIcons(
                        ft.icons.DASHBOARD_ROUNDED, "Dashboard"),
                    self.ContainedIcons(ft.icons.BAR_CHART, "Revenue"),
                    self.ContainedIcons(
                        ft.icons.NOTIFICATIONS, "Notifications"),
                    self.ContainedIcons(
                        ft.icons.PIE_CHART_ROUNDED, "Analytics"),
                    ft.Divider(height=5, color="white54"),
                    self.ContainedIcons(ft.icons.SETTINGS, "Settings"),
                    self.ContainedIcons(ft.icons.LOGOUT_ROUNDED, "Logout"),

                ]
            )
        )
