import click
import pandas as pd
from .transcoding.names_map import col_names
from .transcoding.metadata import dtype


worldometer_covid_stats_url = (
    "https://web.archive.org/web/20200309183200/"
    "https://www.worldometers.info/coronavirus/coronavirus-age-sex-demographics/"
)

numerics_perc_col = ["death_rate_confirmed_rel_freq", "death_rate_all_rel_freq"]


def prepare_worldometers_table(df, numerics_perc_col):
    df = df.rename(columns=col_names)
    for col in numerics_perc_col:
        df[col] = df[col].str.replace("[A-z\% ]+", "")
        df[col] = df[col].replace("", "0.")
        df[col] = df[col].astype(float) / 100

    if "gender" in df.columns:
        df["gender"] = df["gender"].replace("Male", "males")
        df["gender"] = df["gender"].replace("Female", "females")

    return df


def parse_worldometers_stats(worldometer_covid_stats_url=worldometer_covid_stats_url):

    covid_age, covid_gender, covid_condition = pd.read_html(
        worldometer_covid_stats_url, header=0
    )[2:5]

    covid_age, covid_gender, covid_condition = [
        prepare_worldometers_table(df, numerics_perc_col)
        for df in (covid_age, covid_gender, covid_condition)
    ]

    return covid_age, covid_gender, covid_condition
