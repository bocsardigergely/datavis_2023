from dash import dcc, html
import dash_bootstrap_components as dbc
import base64
from ..config import color_list1, color_list2
import os


class DashBoard:
    def __init__(self, df):
        self.df = df
        self.positions = df['position'].unique().tolist()
        self.cards = self.create_cards()
        self.filtered_cards = self.cards[self.positions[0]]

    def create_cards(self):
        cards_dict = {
            'GK': [],
            'DF': [],
            'MF': [],
            'FW': []
        }
        for index, row in self.df.iterrows():
            encoded_image = base64.b64encode(open(row['picture'], 'rb').read())

            card = dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.Div([
                                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={"width": "10%", 'margin': '10px'}),
                                html.H5(row["player"], className="card-title")],
                                style={"display": "flex", "justify-content": "left"}
                            ),
                            html.Div(
                                html.P(f"Position: {row['position']}", className="card-text"),
                                style={"display": "flex", "justify-content": "left", "margin": "0 0 20px 20px"}
                            ),
                        ],

                    )
                ],
                className="shadow rounded"
            )
            cards_dict[row['position']].append(card)
        return cards_dict

    def generate_description_card(self):
        return html.Div(
            id="description-card",
            children=[
                html.H5("Example dashboard"),
                html.Div(
                    id="intro",
                    children="You can use this as a basic template for your JBI100 visualization project.",
                ),
                html.Label("Player positions"),
                dcc.Dropdown(
                    id="select-color-scatter-1",
                    options=[{"label": pos, "value": pos} for pos in self.positions],
                    value=[self.positions[0]],
                    multi=True,
                    clearable=False,
                    optionHeight=35,
                    style={"width": "100%", "padding-bottom": "10px",
                           "font-size": "14px", "color": "#444"},
                    className="dash-bootstrap",
                    placeholder="Select positions",
                ),
                html.Br()
            ],
        )

    def print_cards(self):
        return html.Div(
            id="control-card",

            children=[
                html.Div(self.filtered_cards, className="card-deck"),
            ], style={"textAlign": "float-left"}
        )

    def update(self, dropdown_value):
        # Assuming dropdown_value is a list of positions
        new_cards = []
        for position in dropdown_value:
            new_cards += self.cards[position]

        self.filtered_cards = new_cards

    def make_menu_layout(self):
        return [self.generate_description_card(), self.print_cards()]
