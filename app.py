from jbi100_app.main import app
from jbi100_app.views.menu import DashBoard
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.data import load_data
from dash import html
from dash.dependencies import Input, Output


if __name__ == '__main__':
    # Create data
    df = load_data()

    # Instantiate custom views
    scatterplot1 = Scatterplot("All players", 'minutes_90s', 'goals_per90', df, "controls_1")
    scatterplot2 = Scatterplot("Team", 'minutes_90s', 'goals_per90', df, "controls_2")
    
    dashboard = DashBoard(df)

    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                children=dashboard.make_menu_layout()
            ),

            # Right column
            html.Div(
                id="right-column",
                className="nine columns",
                children=[
                    scatterplot1,
                    scatterplot2
                ],
            ),
        ],
    )

    # Define interactions
    @app.callback(
        Output(scatterplot1.html_id, "figure"), [
        Input("x_axis_controls_1", "value"),
        Input("y_axis_controls_1", "value"),
        Input(scatterplot2.html_id, 'selectedData')
    ])
    def update_scatter_1(selected_x, selected_y, selected_data):
        return scatterplot1.update(selected_x, selected_y, selected_data)

    @app.callback(
        Output(scatterplot2.html_id, "figure"), [
        Input("x_axis_controls_2", "value"),
        Input("y_axis_controls_2", "value"),
        Input(scatterplot1.html_id, 'selectedData')
    ])
    def update_scatter_2(selected_x, selected_y, selected_data):
        return scatterplot2.update(selected_x, selected_y, selected_data)

    @app.callback(
        Output('control-card', 'children'),
        [Input('select-color-scatter-1', 'value')]
    )
    def update_card_deck(dropdown_value):
        dashboard.update(dropdown_value)
        return dashboard.print_cards()

    app.run_server(debug=False, dev_tools_ui=False)