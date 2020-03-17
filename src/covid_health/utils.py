import os
import requests
import gzip
import pandas as pd
import csv
from .transcoding.names.human import lang


def map_names(item, language="it", source="eurostat"):
    if isinstance(item, str):
        return lang[language].get(item, item)
    if isinstance(item, pd.DataFrame):
        return item.rename(columns=lang[language]["col"])
    if isinstance(item, pd.Series):
        if source == "eurostat":
            from .transcoding.names.eurostat import var
            return item.replace(dict(var["eurostat"][item.name]))
        else:
            return item.replace(lang[language].get(item.name, {}))


def download_and_parse_gzip_csv(url, params: dict = {}):
    response = requests.get(url, params=params)
    data = gzip.decompress(response.content).decode()
    data = data.replace(",", "\t")
    data = csv.DictReader(data.split("\n"), delimiter="\t")
    return data


def download_csv(url):
    response = requests.get(url)
    data = csv.DictReader(
        [line.decode("latin-1") for line in response.iter_lines()], delimiter=";"
    )
    return data


def parse_panel(df, value_name="value"):
    time = df.filter(regex="[1-2][0-9]{3}").columns
    nontime = df.filter(regex="^((?![1-2][0-9]{3}).)*$").columns
    df = df.melt(id_vars=nontime, value_vars=time, var_name="time")
    df = df.rename(columns={"geo\\time": "geo"})
    return df


def parse_pivoted(df, value_name):
    df = df.stack(list(range(len(df.columns.levels))))  # stack all columns
    df.name = value_name
    df = df.reset_index()
    return df


def convert_dtype(df, dtype):
    return df.astype({col: dtype.get(col, dt) for col, dt in df.dtypes.items()})

