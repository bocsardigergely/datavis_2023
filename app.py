from jbi100_app.main import app
from jbi100_app.views.checklist import PlayerList
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.pcpplot import PCPplot
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import os

# if using macos
from jbi100_app.data_loader_macos import load_data
# # location of data:
os.chdir("/Users/gbocsardi/Documents/2. areas/sem_4/dataviz/example")

# if using windows
# from jbi100_app.data_loader_windows import load_data
# # location of data:
# os.chdir(r"D:\Data Science and Entrepreneurship MSc\DV - Data Visualiztation\JM0250 Data (2022-2023)")


# IMPORTNANT NOTE: adjust the working directory to the root of the project in either data_loader.py or data.py


if __name__ == '__main__':
    # Create data
    df = load_data()
    df = df.fillna(0)

    # Instantiate custom views
    scatterplot1 = Scatterplot("Chosen team", 'minutes_90s', 'goals_per90', df, "controls_1", 'rgba(200,0,0,0.8)')
    scatterplot2 = Scatterplot("All players", 'minutes_90s', 'goals_per90', df, "controls_2", 'rgba(0,0,200,0.8)')
    pcpplot = PCPplot("Group averages", df) 
    player_list = PlayerList(df)

    # Set up page layout
    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="two columns",
                children=[
                    html.H5("Player List"),
                    html.H6("Choose players to add to your team!"),
                    player_list.checklist,
                ],
                style={"overflow": "scroll"}
            ),

            # Right column
            html.Div(
                id="right-column",
                className="ten columns",
                children=[
                    html.Div(
                        id="upper-blob",
                        children=[
                            dbc.Row([
                                dbc.Col([
                                    scatterplot1
                                ], width=6),
                                dbc.Col([
                                    scatterplot2
                                ], width=6)
                            ])
                        ]
                    ),
                    html.Div(
                        id="lower-blob",
                        children=[
                            pcpplot
                        ]
                    ),
                    html.Div(id = 'hidden-div', style={'display':'none'}),
                ]
            )
        ]
    )


    # Selected team scatterplot
    @app.callback(
        Output(scatterplot1.html_id, "figure"), [
        Input("x_axis_controls_1", "value"),
        Input("y_axis_controls_1", "value"),
        Input("hidden-div", "children"),
        Input("player-checklist", "value")
    ])
    def update_scatter_1(selected_x, selected_y, selected_data, player_list):
        return scatterplot1.update(selected_x, selected_y, selected_data, player_list)

    # Full team scatterplot
    @app.callback(
        Output(scatterplot2.html_id, "figure"), [
        Input("x_axis_controls_2", "value"),
        Input("y_axis_controls_2", "value"),
        Input(scatterplot1.html_id, 'selectedData'),
        Input("hidden-div", "children")
    ])
    def update_scatter_2(selected_x, selected_y, selected_data, player_list):
        return scatterplot2.update(selected_x, selected_y, selected_data, player_list)

    #PCPlot
    @app.callback(
        Output(pcpplot.html_id, "figure"), [
        Input("player-checklist", "value"),
    ])
    def update_pcp(player_list):
        return pcpplot.update(player_list)

    app.run_server(debug=False, dev_tools_ui=False)