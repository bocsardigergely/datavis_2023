from dash import dcc, html
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


class Scatterplot(html.Div):
    def __init__(self, name, feature_x, feature_y, df, control_id, color):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.og_df = df
        self.attribute_list = df.columns
        self.feature_x = feature_x
        self.feature_y = feature_y
        self.color = color

        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                self.generate_axis_control_card(control_id),
                dcc.Graph(id=self.html_id, figure={"layout": {"height": 300}})
            ],
        )

    
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
            style={"textAlign": "left", 'margin-bottom': 10, 'margin-top':10},
        )

    def update(self, x_axis, y_axis, selected_data, player_list = None):
        self.fig = go.Figure()

        if player_list:
            self.df = self.og_df[self.og_df['player'].isin(player_list)]

        self.feature_x = x_axis
        self.feature_y = y_axis

        x_values = self.df[self.feature_x]
        y_values = self.df[self.feature_y]
        self.fig.add_trace(go.Scatter(
            x=x_values, 
            y=y_values,
            mode='markers',
            marker_color='rgb(200,200,200)',
            hovertext=self.df['player']
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
            selected=dict(marker=dict(color=self.color)),

            # color of unselected pts
            unselected=dict(marker=dict(color='rgb(200,200,200)', opacity=0.9))
        )

        # update axis titles
        self.fig.update_layout(
            xaxis_title=self.feature_x,
            yaxis_title=self.feature_y,
        )

        self.fig.update_layout(
            margin=dict(l=30, r=30, t=20, b=20),
        )

        return self.fig
