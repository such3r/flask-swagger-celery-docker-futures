import json
import pandas as pd
import hashlib

import plotly
import plotly.graph_objects as go
import plotly.express as px
# from plotly.subplots import make_subplots

from dateutil.relativedelta import relativedelta
from typing import Union, Tuple

from .subsystems.tasks import celery
from src.subsystems.database import mongodb_client


def make_seasonality(data: pd.DataFrame) -> pd.DataFrame:
    closes = data[["close"]].copy()

    deltas = [0, 1, 5, 10, 15]
    delta_names = ["All time", "Year to date", "Five years", "Ten years", "Fifteen years"]
    components = []

    for d in deltas:
        if d > 0:
            cutoff = closes.index[-1] - relativedelta(years=d)
            shrunk = closes.loc[closes.index > cutoff]
        else:
            shrunk = closes

        agg = shrunk.groupby([shrunk.index.month, shrunk.index.day]).mean()
        components.append(agg)

    seasonality = pd.concat(components, axis=1)
    seasonality.columns = delta_names
    seasonality.index = seasonality.index.map(lambda x: "2000/" + "/".join(["%.2d" % v for v in x]))
    seasonality.index = pd.to_datetime(seasonality.index)
    seasonality.index = seasonality.index.strftime("%b %d")
    return seasonality


def read_history_from_file(file) -> pd.DataFrame:
    data: pd.DataFrame = pd.read_csv(file,
                                     names=['NA', 'date', 'open', 'high', 'low', 'close'],
                                     index_col=1,
                                     ).drop(columns=['NA'])

    data.index = pd.to_datetime(data.index)
    return data


def hash_file(file) -> str:
    file_hash = hashlib.md5()

    while chunk := file.read(8192):
        file_hash.update(chunk)

    return file_hash.hexdigest()  # to get a printable str instead of bytes


def read_file_with_hash(file) -> (str, str):
    file_hash = hash_file(file)
    file.seek(0)
    data = read_history_from_file(file)
    file.seek(0)
    return file_hash, data.to_json()


@celery.task
def add_file_to_database(file_hash: str, contents: str):
    data = mongodb_client.db["data"]
    data_title = {"hash": file_hash}
    data_contents = data_title
    data_contents.update({"contents": contents})

    # print(data.find_one(data_title))

    if data.find_one(data_title):
        pass
        # data.update_one(data_title, data_contents)
    else:
        data.insert_one(data_contents)

    log = mongodb_client.db["log"]
    log_title = {"last": "file"}
    log_data = log_title
    log_data.update({"hash": file_hash})
    print(log_data)

    if log.find_one(log_title):
        pass
        # log.update_one(log_title, log_data)
    else:
        log.insert_one(log_data)

    print(log.find_one(log_title))


def find_last_hash() -> Union[str, None]:
    file_hash = mongodb_client.db["log"].find_one({"last": "file"})

    if file_hash:
        return file_hash["hash"]

    return None


def read_last_history() -> Union[pd.DataFrame, None]:
    return read_history_by_id(find_last_hash())


def read_history_by_id(id: Union[str, None]) -> Union[pd.DataFrame, None]:
    if id is None:
        return None

    json_contents = mongodb_client.db["data"].find_one({"hash": id})["contents"]
    return pd.read_json(json_contents)


@celery.task
def remove_history_by_id(id: str):
    mongodb_client.db["data"].remove({"hash": id})


def plot_graph(data: pd.DataFrame) -> (go.Figure, go.Figure):
    seasonality = make_seasonality(data)
    candlestick = go.Figure(data=[go.Candlestick(x=data.index,
                                                 open=data["open"],
                                                 high=data["high"],
                                                 low=data["low"],
                                                 close=data["close"],)])
    candlestick.update_layout(title="Price history")
    lines = px.line(seasonality, x=seasonality.index, y=seasonality.columns)
    lines.update_layout(title="Seasonality")
    return (candlestick, lines)


@celery.task
def plot_graph_from_id(id: Union[str, None]) -> Union[Tuple[str], None]:
    data = read_history_by_id(id)

    if data is None:
        return None

    figs = plot_graph(data)
    graphs_json = tuple([json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) for fig in figs])
    return graphs_json


def plot_last_graph() -> Union[Tuple[str], None]:
    id = find_last_hash()
    return plot_graph_from_id(id)
