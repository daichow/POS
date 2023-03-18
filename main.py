

# ---------------------------------------------

# # define the name of the CSV file and the delimiter
# filename = "menu.csv"
# delimiter = ","

# # define the rows to be appended to the sheet
# new_rows = [
#     ["Salad", "Small salad", "4.99"],
#     ["Salad", "Large salad", "7.99"]
# ]

# # read the existing data in the sheet
# data = sheet.get_all_values()

# # convert the data to a pandas dataframe
# df = pd.DataFrame(data)

# # write the dataframe to a CSV file
# df.to_csv(filename, index=False, header=False, sep=delimiter, mode='a')

# # append the new rows to the sheet
# for row in new_rows:
#     sheet.append_row(row)

# # print the updated data in the sheet
# data = sheet.get_all_values()
# print(data)

# __________________________________________________________________________

# Flet dropdown tutorial

import flet as ft

# two parts: a top and bottom


class MainContainer(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        return ft.Container(
            width=275,
            height=60,
            content=ft.Column(
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "Modern Dropdown Control",
                        size=10,
                        weight='w400',
                        color='white54',

                    ),
                    ft.Text(
                        "Line Indent",
                        size=30,
                        weight='bold',
                        color='white54',

                    )
                ]
            )
        )


class DropdownContainer(ft.UserControl):
    def __init__(self, initials, name, gen, title, description, salary):
        self.initials = initials
        self.name = name
        self.gen = gen

        self.title = title
        self.description = description
        self.salary = salary
        super().__init__()

    def ExpandContainer(self, e):
        if self.controls[0].height != 180:
            self.controls[0].height = 180
            self.controls[0].update()
        else:
            self.controls[0].height = 90
            self.controls[0].update()

    def TopContainer(self):
        return ft.Container(
            width=265,
            height=70,
            # bgcolor='pink',
            content=ft.Column(
                spacing=0,
                controls=[
                    ft.Row(controls=[
                        ft.Container(
                            width=40,
                            height=40,
                            bgcolor='white24',
                            border_radius=40,
                            alignment=ft.alignment.center,
                            content=ft.Text(
                                self.initials, size=11, weight='bold')
                        ),
                        ft.VerticalDivider(width=2),
                        ft.Container(
                            content=ft.Column(
                                spacing=1,
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(self.name, size=11),
                                    ft.Text(self.gen, size=9, color='white54')
                                ]
                            )
                        )
                    ]),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.icons.ARROW_DROP_DOWN_CIRCLE_ROUNDED,
                                    icon_size=20,
                                    on_click=lambda e: self.ExpandContainer(e),

                                )
                            )
                        ]
                    )
                ]
            )
        )

    def GetEmployeeData(self):
        items = [
            ['Job Title', self.title],
            ['Description', self.description],
            ['Salary', self.salary]
        ]
        l = []
        for item in items:
            l.append(ft.Row(
                controls=[
                    ft.Column(
                        expand=1,  # 1:2 expand ratio
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Text(item[0], size=9, weight='bold')
                        ]
                    ),
                    ft.Column(
                        expand=2,  # 1:2 expand ratio
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Text(item[1], size=9,
                                    weight='bold', color='white54')
                        ]
                    )
                ]
            ))

        return l

    def BottomContainer(self):
        title, description, salary = self.GetEmployeeData()
        return ft.Container(
            width=265,
            height=100,
            content=ft.Column(
                spacing=12,
                controls=[
                    title,
                    description,
                    salary
                ]
            )
        )

    def build(self):
        return ft.Container(
            width=275,
            height=90,
            bgcolor='white10',
            border_radius=11,
            animate=ft.animation.Animation(400, 'decelerate'),
            padding=ft.padding.only(left=10, right=10, top=10),
            # clips contents to container, cancels overflow, costly productionwise
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.TopContainer(),
                    self.BottomContainer()
                ]
            )
        )


def main(page: ft.Page):
    page.title = "Flet Modern Dropdown"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    main_container = ft.Container(
        width=280,
        height=600,
        bgcolor='black',
        border_radius=40,
        padding=20,
        content=ft.Column(
            scroll='hidden',
            controls=[
                ft.Divider(height=20, color='transparent'),
                MainContainer(),
                ft.Divider(height=30, color='white24'),
                ft.Text('Employees', size=12),
                DropdownContainer("M.C", "Mahir Chowdhury", "Engineer",
                                  "Senior Software Engineer", "Full Stack", "$120, 000"),
                DropdownContainer("K.W", "Kevin White", "Designer",
                                  "UI/UX Engineer", "Front End", "$95,000")

            ]
        )
    )
    page.add(main_container)
    page.update()


ft.app(target=main)
