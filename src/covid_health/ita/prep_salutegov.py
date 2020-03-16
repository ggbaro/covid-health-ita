import os
import click

import requests
import csv
import pandas as pd
import numpy as np

from ..transcoding.names.ita import col
from ..transcoding.metadata import dtype

from ..utils import download_csv, convert_dtype


# url_posti_letto = "http://www.dati.salute.gov.it/imgs/C_17_dataset_18_0_upFile.csv"
url_salute_gov = "http://www.dati.salute.gov.it/imgs/{}"
# url_hospital_metadata = "http://www.dati.salute.gov.it/imgs/C_17_dataset_2_0_upFile.csv"

figures = {"hospital_beds_by_discipline_hospital": "C_17_dataset_96_0_upFile.csv"}


def parse_dataset(
    figure="hospital_beds_by_discipline_hospital", verbose=0, col=col, dtype=dtype
):

    # Retrieve and read file
    df = pd.DataFrame(download_csv(url_salute_gov.format(figures[figure])))
    df = df.rename(columns=col[figure])

    dtype = {col: tp for col, tp in dtype.items() if col in df.columns}

    stringlike = [col for col, tp in dtype.items() if tp == str]
    numlike = [col for col, tp in dtype.items() if tp in (int, float)]

    # Adjust data
    df = df.replace("N.D.", "0")

    # trim repeated white space
    for field in stringlike:
        df[field] = (
            df[field].str.replace(r"[ ]{2,}", r" ").str.strip()
        )

    # replace decimal and thousands sep
    for field in numlike:
        df[field] = (
            df[field].str.replace(r".", r"").str.replace(r",", r".")
        )

    # adjust dtypes
    df = df.astype(dtype)

    if verbose > 0:
        print(df)
        df.info(verbose=verbose)
    
    df = convert_dtype(df, dtype)

    return df


# --- CLI ---


@click.group()
def cli():
    pass


@cli.command(name="from-webrepo", help="choose figure between {}".format(list(figures.keys())))
@click.argument("figure", default="hospital_beds_by_discipline_hospital")
@click.option("--out-fp", default="./data/interim/ministero-salute/",
              help="if not specified, defaults to 'dataset_name.csv'",)
def dataset_to_csv(figure, out_fp):

    if np.all(
        [
            ext not in out_fp.rsplit("/", 1)[-1]
            for ext in (".csv", ".csv.gz", ".csv.zip")
        ]
    ):
        out_fp = os.path.join(out_fp, figure + ".csv")
    os.makedirs(os.path.dirname(out_fp), exist_ok=True)
    print(f"writing: {out_fp}")
    
    df = parse_dataset(figure)         
    df.to_csv(out_fp, index=False)


cli.add_command(dataset_to_csv)


if __name__ == "__main__":
    cli()