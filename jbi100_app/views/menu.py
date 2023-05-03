import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd


def create_menu(df):
    # Get unique values from the 'category' column
    categories = df["category"].unique().tolist()

    # Create an empty list to store the checkbox options
    checkbox_options = []

    # Iterate over the unique categories and create a checkbox for each
    for category in categories:
        checkbox = dbc.CheckboxInput(
            id={"type": "checkbox", "index": category},
            className="mr-1",
            checked=True,  # Default to checked
        )
        label = dbc.Label(category, htmlFor={"type": "checkbox", "index": category})
        checkbox_options.append(dbc.FormGroup([checkbox, label]))

    # Create the dropdown menu with the checkbox options
    dropdown_menu = dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(
                checkbox_options,
                label="Filter by Category",
                style={"min-width": "200px"},
            )
        ],
        label="Filter",
        className="ml-2",
        nav=True,
    )

    # Create the card columns for the filtered rows
    def create_card_columns(checked_categories):
        filtered_df = df[df["category"].isin(checked_categories)]
        card_columns = dbc.CardColumns(
            [
                dbc.Card(
                    [
                        dbc.CardImg(src=row["image_path"]),
                        dbc.CardBody(html.P(row["text"], className="card-text")),
                    ],
                    className="mb-3",
                )
                for index, row in filtered_df.iterrows()
            ]
        )
        return card_columns

    # Create the menu layout
    menu_layout = dbc.Card(
        dbc.CardBody(
            [
                dropdown_menu,
                html.Div(id="card-columns-div"),
            ]
        )
    )

    # Define the callback to update the card columns based on the selected checkboxes
    @app.callback(
        Output("card-columns-div", "children"),
        [Input({"type": "checkbox", "index": ALL}, "checked")],
    )
    def update_card_columns(checked_states):
        checked_categories = [
            category for category, checked in zip(categories, checked_states) if checked
        ]
        if not checked_categories:
            checked_categories = (
                categories  # Display all rows if no checkboxes are checked
            )
        return create_card_columns(checked_categories)

    return menu_layout
