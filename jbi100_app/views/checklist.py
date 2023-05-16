from dash import dcc, html
import base64

# Player checklist for the left column
class PlayerList:
    def __init__(self, df):
        self.df = df
        self.checklist = dcc.Checklist(options = self.create_checklist(), 
                                       id='player-checklist', 
                                       value=['Andries Noppert'], 
                                       labelClassName = "labelStyle",
                                       inputClassName = "inputStyle",
                                       )
        
    def create_checklist(self):
        checklist_items = []
        for index, row in self.df.iterrows():
            encoded_image = base64.b64encode(open(row['picture'], 'rb').read())
            item = {
                'label': [
                    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={"height": "20px", 'margin': '5px'}),
                    html.Span( str(row["player"]) + " | " + "Position: " + str(row['position']), style={"font-size": 12, "padding-left": 10})
                ],
                'value': row['player']

            }
            checklist_items.append(item)
        return checklist_items