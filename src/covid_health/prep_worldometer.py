import os
import click
import pandas as pd
from datetime import datetime
from .transcoding.names.worldometers import col, val


worldometer_covid_url = (
    "https://web.archive.org/web/{}/" "https://www.worldometers.info/coronavirus/{}"
)

figures = dict(
    age_sex_demographics="coronavirus-age-sex-demographics", countries="#countries",
)


def prepare_worldometers_table(df, figure, col=col):
    df = df.rename(columns=col[figure])

    val_replacements = val[figure]
    for column, old, new in val_replacements:
        if column in df.columns:
            df[column] = df[column].str.replace(old, new)

    # we handle rel freqs properly
    if figure == "age_sex_demographics":
        for col in [c for c in df.columns if "_rel_freq" in c]:
            try:
                df[col] = df[col].astype(float) / 100
            except ValueError:
                print(f" +++ error for {col}")
                pass

    return df


def parse_worldometers_stats(
    figure="countries", snapshot_date=f"{datetime.now():%Y%m%d%H}"
):

    tables = pd.read_html(
        worldometer_covid_url.format(snapshot_date, figures[figure]), header=0
    )[2:5]  # this to exclude web.archive.org info tables

    tables = [prepare_worldometers_table(df, figure) for df in tables]
    
    for table in tables:
        print(table)

    return tables



# --- CLI ---


@click.command(name="from-web", help="""Datasets creation from `worldometers.info`.
    Choose figure between {}""".format(list(figures.keys())))
@click.argument("figure")
@click.option("--snapshot-date", default=f"{datetime.now():%Y%m%d%H}")
@click.option("--out-dir", default="./data/interim/worldometers/",
              help="if not specified, defaults to '<figure>.csv'",)
def cli(figure, snapshot_date, out_dir):
    
    os.makedirs(out_dir, exist_ok=True)
    print(f"writing: {out_dir}{figure}_*.csv")
    
    dfs = parse_worldometers_stats(figure, snapshot_date=snapshot_date)         
    for n, df in enumerate(dfs):
        df.to_csv(os.path.join(out_dir, f'{figure}_{n}.csv'), index=False)


if __name__ == "__main__":
    cli()
