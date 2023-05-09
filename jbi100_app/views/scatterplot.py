from dash import dcc, html
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from ..config import color_list1, color_list2, attribute_list
import base64


class Scatterplot(html.Div):
    def __init__(self, name, feature_x, feature_y, df, control_id):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.attribute_list = df.columns
        self.feature_x = feature_x
        self.feature_y = feature_y

        controls = self.generate_axis_control_card(control_id)
        pictures = self.generate_image_list(control_id)

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                pictures,
                controls,
                dcc.Graph(id=self.html_id)
            ],
        )

    def generate_image_list(self, id):

        cards = []

        for index, row in self.df.iterrows():

            encoded_image = base64.b64encode(open(row['picture'], 'rb').read())

            card = dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.Div(
                                [html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={"width": "100%"})]
                            ),
                        ],
                    )
                ]
            )
            cards.append(card)

        row = dbc.Row([dbc.Col(card, width=1) for card in cards])

        return html.Div(children=[row])


    
    def generate_axis_control_card(self, id):
        """

        :return: A Div containing controls for graphs.
        """
        return html.Div(
            id=id,
            children=[
                dbc.Row([
                    dbc.Col([
                        html.Label("X axis"),
                        dcc.Dropdown(
                            id="x_axis_"+id,
                            options=[{"label": i, "value": i} for i in self.attribute_list],
                            value=self.attribute_list[4],
                        )
                    ], width=6),
                    dbc.Col([
                        html.Label("Y axis"),
                        dcc.Dropdown(
                            id="y_axis_"+id,
                            options=[{"label": i, "value": i} for i in self.attribute_list],
                            value=self.attribute_list[6],
                        )
                    ], width=6)
                ])
            ],
            style={"textAlign": "left"}
        )

    def update(self, x_axis, y_axis, selected_data):
        self.fig = go.Figure()

        self.feature_x = x_axis
        self.feature_y = y_axis

        x_values = self.df[self.feature_x]
        y_values = self.df[self.feature_y]
        self.fig.add_trace(go.Scatter(
            x=x_values, 
            y=y_values,
            mode='markers',
            marker_color='rgb(200,200,200)'
        ))
        self.fig.update_traces(mode='markers', marker_size=10)
        self.fig.update_layout(
            yaxis_zeroline=False,
            xaxis_zeroline=False,
            dragmode='select'
        )
        self.fig.update_xaxes(fixedrange=True)
        self.fig.update_yaxes(fixedrange=True)

        # highlight points with selection other graph
        if selected_data is None:
            selected_index = self.df.index  # show all
        else:
            selected_index = [  # show only selected indices
                x.get('pointIndex', None)
                for x in selected_data['points']
            ]

        self.fig.data[0].update(
            selectedpoints=selected_index,

            # color of selected points
            selected=dict(marker=dict(color='seagreen')),

            # color of unselected pts
            unselected=dict(marker=dict(color='rgb(200,200,200)', opacity=0.9))
        )

        # update axis titles
        self.fig.update_layout(
            xaxis_title=self.feature_x,
            yaxis_title=self.feature_y,
        )

        return self.fig
