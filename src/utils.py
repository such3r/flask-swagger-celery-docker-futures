import json
import plotly
import pandas as pd
import plotly.graph_objects as go

def read_history_by_id(id: str) -> pd.DataFrame:
    data = pd.read_csv("../examples/data/KC-057.CSV",
                       names=['NA', 'date', 'open', 'high', 'low', 'close'],
                       index_col=1,
    ).drop(columns=['NA'])
    return data

def plot_graph(data: pd.DataFrame) -> go.Figure:
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                         open=data['open'],
                                         high=data['high'],
                                         low=data['low'],
                                         close=data['close'])])
    return fig

def plot_graph_from_id(id: str) -> str:
    data = read_history_by_id(id)
    fig = plot_graph(data)
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json