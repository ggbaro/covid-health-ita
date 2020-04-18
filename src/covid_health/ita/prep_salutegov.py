import os

import click
import numpy as np
import pandas as pd

from covid_health.transcoding.metadata import dtype
from covid_health.transcoding.names.ita import col
from covid_health.utils import convert_dtype, download_and_parse_zip_csv, download_csv

url_salute_gov = "http://www.dati.salute.gov.it/imgs/{}"

figures = {
    "hospital_beds_by_discipline_hospital": "C_17_dataset_96_0_upFile.csv",
    "asl_expenditure_by_device_2012": "C_17_dataset_63_download_itemDownload_0_upFile.csv",  # noqa: E501
    "asl_expenditure_by_device_2013": "C_17_dataset_71_download_itemDownload_0_upFile.zip",  # noqa: E501
    "asl_expenditure_by_device_2014": "C_17_dataset_78_download_itemDownload_0_upFile.zip",  # noqa: E501
    "asl_expenditure_by_device_2015": "C_17_dataset_81_download_itemDownload_0_upFile.zip",  # noqa: E501
    "asl_expenditure_by_device_2016": "C_17_dataset_91_download_itemDownload_0_upFile.zip",  # noqa: E501
    "asl_expenditure_by_device_2017": "C_17_dataset_97_download_itemDownload_0_upFile.zip",  # noqa: E501
    "asl_comuni_pop": "C_17_dataset_3_0_upFile.csv",
    "pharmacies": "C_17_dataset_5_download_itemDownload0_upFile.CSV",
}
col = col["salutegov"]


def parse_dataset(
    figure="hospital_beds_by_discipline_hospital", verbose=0,
):
    if figure not in figures.keys():
        raise NotImplementedError(
            f"Figure '{figure}' not regognized.\nChoose one of {figures.keys()}"  # noqa: E501
        )
    url = url_salute_gov.format(figures[figure])
    # Retrieve and read file
    if url.endswith(".zip"):
        df = pd.DataFrame(
            download_and_parse_zip_csv(url, encoding="latin-1", delimiter=";")
        )
    else:
        df = pd.DataFrame(download_csv(url, encoding="latin-1", delimiter=";"))

    df = df.rename(columns=col)

    if "region_code" in df.columns:
        df.loc[df["region_code"].apply(len) == 3, "region_code"] = df.loc[
            df["region_code"].apply(len) == 3, "region_code"
        ].str[:-1]

    for col_ in ["latitude", "longitude"]:
        if col_ in df.columns:
            # df[col_] = df[col_].str.replace(",", ".")
            df[col_] = df[col_].str.replace("^ {0,}- {0,}$", "", regex=True)
            df[col_] = df[col_].replace("", np.nan)

    dtype_ = {col: tp for col, tp in dtype.items() if col in df.columns}
    stringlike = [col for col, tp in dtype_.items() if tp == str]
    numlike = [col for col, tp in dtype_.items() if tp in (int, float)]

    # Adjust data
    df = df.replace("N.D.", "0")

    # trim repeated white space
    for field in stringlike:
        df[field] = df[field].str.replace(r"[ ]{2,}", r" ").str.strip()

    # replace decimal and thousands sep
    for field in numlike:
        df[field] = df[field].str.replace(r".", r"").str.replace(r",", r".")

    if verbose > 0:
        print(df)
        df.info(verbose=verbose)

    df = convert_dtype(df, dtype_)

    return df


# --- CLI ---


@click.group()
def cli():
    pass


@cli.command(
    name="from-webrepo", help="choose figure between {}".format(list(figures.keys())),
)
@click.argument("figure", default="hospital_beds_by_discipline_hospital")
@click.option(
    "--out-fp",
    default="./data/interim/ministero-salute/",
    help="if not specified, defaults to 'dataset_name.csv'",
)
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
