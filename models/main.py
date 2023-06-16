import flet as ft
import flet_mvc

# from api import read_xml_files
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from flet_mvc import data

from flet_mvc import FletModel, data

# Model


class Model(FletModel):
    def __init__(self):
        # References
        self.info = ft.Ref[ft.Text]()
        self.menu_list_view = ft.Ref[ft.GridView]()
        self.cart_list_view = ft.Ref[ft.Column]()
        self.text = ft.Ref[ft.Text]()

        self.cash_button = ft.Ref[ft.Container]()
        self.card_button = ft.Ref[ft.Container]()

        self.subtotal = ft.Ref[ft.Text]()
        self.discount = ft.Ref[ft.TextField]()
        self.tax = ft.Ref[ft.Text]()
        self.total = ft.Ref[ft.Text]()
        self.change_column = ft.Ref[ft.Column]()

        self.images = []

        self.WIDTH = 1000
        self.HEIGHT = 700

        self.cart_list = []

        # [Optional]
        self.controller = None

        # Set the name of the credentials file
        self.credentials_file = "./assets/universitypizza.json"

        # Define the scope of the API access
        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]

        # Authenticate the credentials file
        self.creds = Credentials.from_service_account_file(
            self.credentials_file, scopes=self.scope
        )

        # Authorize access to the spreadsheet
        self.client = gspread.authorize(self.creds)

        print("MAKING A REQUEST TO SHEETS")
        # Open the sheet by name
        self.menu_sheet = self.client.open("University Pizza").worksheet("Menu")
        # self.sales_sheet = self.menu_sheet = self.client.open(
        #     "University Pizza"
        # ).worksheet("Sales")
        # Get all the data from the sheet
        self.menu_data = self.menu_sheet.get_all_values()

        self.toppings = [
            s.split(",")[1]
            for s in self.menu()
            if s.startswith("Meat Toppings")
            or s.startswith("Veggie Toppings")
            or s.startswith("Sauces")
        ]

        self.pizzas = [s.split(",")[1] for s in self.menu() if s.startswith("Pizza")]

    @data
    def menu(self):
        # Convert the data to a Pandas dataframe
        df = pd.DataFrame(self.menu_data[1:], columns=self.menu_data[0])

        string_list = df.apply(lambda row: ",".join(map(str, row)), axis=1).tolist()
        # Print the dataframe
        # print(df)
        return string_list
