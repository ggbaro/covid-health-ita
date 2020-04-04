import click
import os
import pandas as pd
from covid_health.transcoding.names.ita import col, var
from covid_health.transcoding.metadata import dtype
from covid_health.utils import download_and_parse_gzip_csv


url_istat = "http://dati.istat.it/DownloadFiles.aspx?&DatasetCode={}&Lang=IT"

figures = {
    "death_causes": url_istat.format("DCIS_CMORTE1_RES"),
}

gz_figures = {
    "2019_pop_regions": "http://demo.istat.it/pop2019/dati/regioni.gz",
    "2018_pop_regions": "http://demo.istat.it/pop2018/dati/regioni.gz",
    "2019_pop_province": "http://demo.istat.it/pop2019/dati/province.gz",
}


figure = "2018_pop_regions"


def parse_istat_geodemo(figure, dtype=dtype, col=col["istat"]):
    """Extract one of {}
    """.format(
        list(gz_figures.keys())
    )
    time = pd.to_datetime(figure[:4]) if figure.startswith("20") else None
    url = gz_figures[figure]
    df = pd.DataFrame(
        list(
            download_and_parse_gzip_csv(url, delimiter=",", eurostat=False, skiprows=1)
        )
    )
    df = df.filter(regex="Regione|Età|Provincia|Totale[\w ]+")  # noqa: W605
    df = df.rename(columns=col)
    df = df.loc[(df != "Totale").all(axis=1)]
    df = df.melt(
        id_vars={"age", "region", "province"}.intersection(df.columns),
        var_name="sex",
        value_name="population",
    )
    if time:
        df["time"] = time
    return df


def parse_istat_dataset(df, col=col, dtype=dtype):

    if isinstance(df, str):
        df = pd.read_csv(df, dtype={"Codice Comune": str}, parse_dates=["TIME"])

    df = df.rename(columns=col["istat"])

    for column, old, new in var["istat"]:
        if column in df.columns:
            df[column] = df[column].str.replace(old, new)

    # for column in df.columns:
    #     df = df.loc[df[column] != "total"]

    # filter specified columns
    df = df.loc[:, set(col["istat"].values()).intersection(df.columns)]

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
