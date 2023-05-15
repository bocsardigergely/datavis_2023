from dash import dcc, html
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
import pandas as pd


class PCPplot(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-") + "pcp"
        self.df = df
        self.attributes = ['age', 'minutes', 'passes_completed', 'shots_on_target_per90', 'assists_per90', 'goals_per90']
        self.list1 = []
        self.list2 = df['player'].unique()

        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )

    def calculate_averages(self, players_list, df):
        subset_df = df[df['player'].isin(players_list)]
        return subset_df[['age', 'minutes', 'passes_completed', 'shots_on_target_per90', 'assists_per90', 'goals_per90']].mean()

    def update(self, player_list):
        
        self.list1 = player_list

        #scaler = MinMaxScaler()
        #print("hjghklájghjfhkjhlihhfg")

        # let's start by calculating the group averages based on the lists
        # which will once be part of the arguments to this function

        data = {
            'players_list': ['list1', 'list2'],
            'age': [self.calculate_averages(self.list1, self.df)['age'], self.calculate_averages(self.list2, self.df)['age']],
            'minutes': [self.calculate_averages(self.list1, self.df)['minutes'], self.calculate_averages(self.list2, self.df)['minutes']],
            'passes_completed': [self.calculate_averages(self.list1, self.df)['passes_completed'], self.calculate_averages(self.list2, self.df)['passes_completed']],
            'shots_on_target_per90': [self.calculate_averages(self.list1, self.df)['shots_on_target_per90'], self.calculate_averages(self.list2, self.df)['shots_on_target_per90']],
            'assists_per90': [self.calculate_averages(self.list1, self.df)['assists_per90'], self.calculate_averages(self.list2, self.df)['assists_per90']],
            'goals_per90': [self.calculate_averages(self.list1, self.df)['goals_per90'], self.calculate_averages(self.list2, self.df)['goals_per90']]
        }

        avg_df = pd.DataFrame(data)


        self.fig = go.Figure()

        
        self.fig.add_trace(
            go.Parcoords(
                line = dict(color = avg_df.index, colorscale = [[0,'rgba(200,0,0,0.1)'],[1,'rgba(0,0,200,0.1)']]),
                dimensions = list([
                    dict(range=[self.df['age'].min(),self.df['age'].max()],
                            label='Age', values=avg_df['age']),
                    dict(range=[self.df['minutes'].min(),self.df['minutes'].max()],
                            label='Minutes played', values=avg_df['minutes']),
                    dict(range=[self.df['passes_completed'].min(),self.df['passes_completed'].max()],
                            label='Passes completed', values=avg_df['passes_completed']),
                    dict(range=[self.df['shots_on_target_per90'].min(),self.df['shots_on_target_per90'].max()],
                            label='Shots on target per 90', values=avg_df['shots_on_target_per90']),
                    dict(range=[self.df['assists_per90'].min(),self.df['assists_per90'].max()],
                            label='Assists per 90', values=avg_df['assists_per90']),
                    dict(range=[self.df['goals_per90'].min(),self.df['goals_per90'].max()],
                            label='Goals per 90', values=avg_df['goals_per90']),
                ])
            )
        )

        self.fig.update_layout(
            margin=dict(l=60, r=60, t=100, b=60),
            height=320
        )


        return self.fig
