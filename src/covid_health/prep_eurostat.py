import csv
import gzip
import os

import click
import pandas as pd
import numpy as np
import requests

from .transcoding.names.eurostat import col
from .transcoding.metadata import dtype
from .utils import download_and_parse_gzip_csv


known_datasets = dict(
    hospital_beds_nuts2=(
        "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?"
        "file=data/hlth_rs_bdsrg.tsv.gz",
        "year",
        "tot_n_hospital_bed",
    ),
    discharged_by_diagnosis_m_nuts2=(
        "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?"
        "file=data/hlth_co_disch1m.tsv.gz",
        "year",
        "n_patients",
    ),
    discharged_by_diagnosis_f_nuts2=(
        "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?"
        "file=data/hlth_co_disch1f.tsv.gz",
        "year",
        "n_patients",
    ),
    population_nuts2=(
        "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?"
        "file=data/demo_r_d3area.tsv.gz",
        "year",
        "population",
    ),
)


def parse_eurostat_dataset(dataset_name, dtype=dtype):
    url, var_name, value_name = known_datasets[dataset_name]
    data = download_and_parse_gzip_csv(url)
    data = pd.DataFrame(data)
    data.columns = [col.strip() for col in data.columns]
    data = data.replace(":", "").replace(": ", "")
    data = data.rename(columns={r"geo\time": "geo"})

    years_cols = set(data.filter(regex="[1-2][0-9]{3}").columns)
    other_cols = set(data.columns).difference(years_cols)

    data = data.melt(
        id_vars=other_cols,
        value_vars=years_cols,
        var_name=var_name,
        value_name=value_name,
    )

    # dtype = {k: v for k, v in dtype.items() if k in data.columns}
    # data = data.astype(dtype)

    return data


# --- CLI ---


# @click.group()
# def cli():
#     pass


# @cli.command(name="from_eurostat", help="one of {}".format(list(known_datasets.keys())))
@click.command(name="from_eurostat", help="one of {}".format(list(known_datasets.keys())))
@click.argument("dataset_name")
@click.option(
    "--out_fp",
    help="if not specified, defaults to 'dataset_name.csv'",
    default="./data/interim/eurostat/",
)
def cli(dataset_name, out_fp):
# def eurostat_to_csv(dataset_name, out_fp):

    if np.all(
        [
            ext not in out_fp.rsplit("/", 1)[-1]
            for ext in (".csv", ".csv.gz", ".csv.zip")
        ]
    ):
        out_fp = os.path.join(out_fp, dataset_name + ".csv")
    os.makedirs(os.path.dirname(out_fp), exist_ok=True)

    print("saving to: ", out_fp)

    data = parse_eurostat_dataset(dataset_name)
    data.to_csv(out_fp, index=False)


# cli.add_command(eurostat_to_csv)


if __name__ == "__main__":
    cli()
