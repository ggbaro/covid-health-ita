import click

import requests
import csv
import pandas as pd

from .transcoding.names_map import col_names
from .transcoding.metadata import dtype


def download_salutegov_csv(url):
    response = requests.get(url)
    data = csv.DictReader(
        [line.decode("latin-1") for line in response.iter_lines()], delimiter=";"
    )
    return data


# url_posti_letto = "http://www.dati.salute.gov.it/imgs/C_17_dataset_18_0_upFile.csv"
url_posti_letto = "http://www.dati.salute.gov.it/imgs/C_17_dataset_96_0_upFile.csv"
# url_hospital_metadata = "http://www.dati.salute.gov.it/imgs/C_17_dataset_2_0_upFile.csv"


def parse_posti_letto(url_posti_letto=url_posti_letto, verbose=0, dtype=dtype):

    # Retrieve and read file
    posti_letto = pd.DataFrame(download_salutegov_csv(url_posti_letto))
    posti_letto = posti_letto.rename(columns=col_names)

    dtype = {col: tp for col, tp in dtype.items() if col in posti_letto.columns}

    stringlike = [col for col, tp in dtype.items() if tp == str]
    numlike = [col for col, tp in dtype.items() if tp in (int, float)]


    # Adjust data
    posti_letto = posti_letto.replace("N.D.", "0")

    # trim repeated white space
    for field in stringlike:
        posti_letto[field] = (
            posti_letto[field].str.replace(r"[ ]{2,}", r" ").str.strip()
        )

    # replace decimal and thousands sep
    for field in numlike:
        posti_letto[field] = (
            posti_letto[field].str.replace(r".", r"").str.replace(r",", r".")
        )

    # adjust dtypes
    posti_letto = posti_letto.astype(dtype)

    if verbose > 0:
        print(posti_letto)
        posti_letto.info(verbose=verbose)

    return posti_letto


# --- CLI ---


@click.group()
def cli():
    pass


@cli.command(name="prep_from_salutegovit")
@click.option(
    "--out_fp", default="./data/interim/ministero-salute/2010-2019_posti_letto_by_province.csv"
)
def posti_letto_to_csv(out_fp):
    posti_letto = parse_posti_letto()
    posti_letto.to_csv(out_fp, index=False)


cli.add_command(posti_letto_to_csv)


if __name__ == "__main__":
    cli()
