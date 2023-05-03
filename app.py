from jbi100_app.main import app
from dash import html
from dash.dependencies import Input, Output
from jbi100_app.views.menu import create_menu


app.layout = html.Div(
    id="app-container",
    children=[
        # First column
        html.Div(
            id="left-column",
            children=[
                create_menu(df),
            ],
        ),
        # Second column
        html.Div(
            id="middle-column",
            children=[
                html.H1("Middle Column"),
            ],
        ),
        # Third column
        html.Div(
            id="right-column",
            children=[
                html.H1("Right Column"),
            ],
        ),
    ],
)

app.run_server(debug=False, dev_tools_ui=False)
