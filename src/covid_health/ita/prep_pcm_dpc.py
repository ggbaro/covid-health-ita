import click
import pandas as pd
from ..transcoding.names.ita import col
from ..transcoding.metadata import dtype


dpc_covid_prov = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv"
dpc_covid_reg = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv"


def parse_covid_data(repo_url, dtype=dtype):
    covid_stats = pd.read_csv(repo_url, parse_dates=["data"])
    covid_stats = covid_stats.rename(columns=col_names)
    dtype = {k: v for k, v in dtype.items() if k in covid_stats.columns}
    covid_stats = covid_stats.astype(dtype)
    return covid_stats
