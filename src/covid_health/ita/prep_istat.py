import os

import click
import numpy as np
import pandas as pd

from covid_health.transcoding.metadata import dtype
from covid_health.transcoding.names.ita import col, var
from covid_health.utils import (
    download_and_parse_gzip_csv,
    download_and_parse_zip_csv,
)

url_istat = "http://dati.istat.it/DownloadFiles.aspx?&DatasetCode={}&Lang=IT"
figures = {
    "death_causes": url_istat.format("DCIS_CMORTE1_RES"),
}
gz_figures = {
    f"{year}_pop_{lb}": f"http://demo.istat.it/pop{year}/dati/{urlpiece}.gz"
    for year in range(2012, 2020)
    for lb, urlpiece in [
        ("regions", "regioni"),
        ("municipalities", "comuni"),
        ("provinces", "province"),
    ]
}
daily_deaths = (
    "https://www.istat.it/it/files//2020/03/dati-comunali-giornalieri-1.zip"
)
col = col["istat"]
dtype = dtype


def parse_istat_geodemo(figure):
    """Extract one of {}
    """.format(
        list(gz_figures.keys())
    )
    time = pd.to_datetime(figure[:4]) if figure.startswith("20") else None
    url = gz_figures[figure]
    df = pd.DataFrame(
        list(
            download_and_parse_gzip_csv(
                url, delimiter=",", eurostat=False, skiprows=1
            )
        )
    )
    df = df.filter(
        regex="Regione|Età|Provincia|Codice|Denominazione|Totale[\w ]+"
    )  # noqa: W605
    df = df.rename(columns=col)
    df = df.loc[(df != "Totale").all(axis=1)]
    df = df.melt(
        id_vars={
            "age",
            "region",
            "province",
            "province_code",
            "municipality",
            "prov_town_code",
        }.intersection(df.columns),
        var_name="sex",
        value_name="population",
    )
    if time:
        df["time"] = time

    if "age" in df.columns:
        try:
            df["age"] = df["age"].astype(int)
            df = df[df["age"] <= 100]
        except Exception:
            df = df[df["age"].astype(int) <= 100]
    
    df["population"] = df["population"].astype(int)

    return df


def parse_daily_deaths():
    df = pd.DataFrame(
        download_and_parse_zip_csv(
            daily_deaths, encoding="latin-1", delimiter=","
        )
    ).rename(columns=col)
    dtype = {
        "region_code": "category",
        "province_code": "category",
        "region": "category",
        "province": "category",
        "municipality": "category",
        "prov_town_code": "category",
        "age": "category",
        "GE": str,
    }
    dtype.update(
        {
            col: float
            for col in df.filter(regex="^MASCHI|FEMMINE|TOTALE").columns
        }
    )
    df = df.astype(dtype)
    df.info()

    tot_reporting = df.groupby("region")["municipality"].nunique()
    tot_reporting.name = "n_municipalities"
    print(tot_reporting)

    id_vars = [
        "region_code",
        "province_code",
        "region",
        "province",
        "municipality",
        "prov_town_code",
        "age",
        "GE",
    ]

    df = df.melt(id_vars=id_vars, value_name="deaths")
    df["deaths"] = df["deaths"].replace(9999.0, np.nan)
    df = df.dropna()

    df["sex"] = df["variable"].str[:-3].astype("category")
    df["sex"] = df["sex"].replace("MASCHI", "male")
    df["sex"] = df["sex"].replace("FEMMINE", "female")
    df = df[df["sex"].values != "TOTALE"]

    df["timestamp"] = (
        "20"
        + df["variable"].str[-2:]
        + "-"
        + df["GE"].str[:2]
        + "-"
        + df["GE"].str[2:]
    )
    df = df.loc[df.timestamp.values != "2015-02-29"]
    df = df.loc[df.timestamp.values != "2017-02-29"]
    df = df.loc[df.timestamp.values != "2018-02-29"]
    df = df.loc[df.timestamp.values != "2019-02-29"]
    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.floor("D")

    df = df.drop(columns=["GE", "variable"])

    # df = df.query("deaths < 9999 & deaths >= 0")
    # missing = df.query("deaths == 9999")
    if "prov_town_code" in df.columns:
        df["prov_town_code"] = df["prov_town_code"].str.replace(
            "^(0{1,})([1-9][0-9]+)$", r"\2"
        )

    df.info()
    return df, (tot_reporting,)


def parse_istat_dataset(df):

    if isinstance(df, str):
        df = pd.read_csv(
            df, dtype={"Codice Comune": str}, parse_dates=["TIME"]
        )

    df = df.rename(columns=col)

    for column, old, new in var["istat"]:
        if column in df.columns:
            df[column] = df[column].str.replace(old, new)

    # for column in df.columns:
    #     df = df.loc[df[column] != "total"]

    # filter specified columns
    df = df.loc[:, set(col.values()).intersection(df.columns)]

    print(df)

    # df = convert_dtype(df, dtype)

    return df


# --- CLI ---


@click.group()
def cli():
    pass


@click.command(
    name="from-csv",
    help="Provide `source`, a file path or internal data shortcut "
    f"(one of {list(figures.keys())}).",
)
@click.argument("source")
@click.option(
    "--out_fp", default="./data/interim/istat/2019_population_by_province.csv"
)
def parse_istat_csv(source_csv_fp, out_fp):
    data = parse_istat_dataset(source_csv_fp)
    os.makedirs(os.path.dirname(out_fp), exist_ok=True)
    data.to_csv(out_fp, index=False)


cli.add_command(parse_istat_csv)


if __name__ == "__main__":
    cli()
