import click

import requests
import csv
import pandas as pd


@click.group()
def cli():
    pass


def download_salutegov_csv(url):
    response = requests.get(url)
    data = csv.DictReader(
        [line.decode("latin-1") for line in response.iter_lines()], delimiter=";"
    )
    return data


def posti_letto_from_salutegov():
    url_posti_letto = "http://www.dati.salute.gov.it/imgs/C_17_dataset_18_0_upFile.csv"

    dtype = {
        "Anno": int,
        "Codice Regione": str,
        "Descrizione Regione": str,
        "Codice Azienda": str,
        "Tipo Azienda": str,
        "Codice struttura": str,
        "Denominazione struttura": str,
        "Indirizzo": str,
        "Codice Comune": str,
        "Comune": str,
        "Sigla provincia": str,
        "Codice tipo struttura": str,
        "Descrizione tipo struttura": str,
        "Tipo di Disciplina": str,
        "Posti letto degenza ordinaria": int,
        "Posti letto degenza a pagamento": int,
        "Posti letto Day Hospital": int,
        "Posti letto Day Surgery": int,
        "Totale posti letto": int,
    }

    stringlike = [
        "Codice Regione",
        "Descrizione Regione",
        "Codice Azienda",
        "Tipo Azienda",
        "Codice struttura",
        "Denominazione struttura",
        "Indirizzo",
        "Codice Comune",
        "Comune",
        "Sigla provincia",
        "Codice tipo struttura",
        "Descrizione tipo struttura",
        "Tipo di Disciplina",
    ]

    numlike = [
        "Posti letto degenza ordinaria",
        "Posti letto degenza a pagamento",
        "Posti letto Day Hospital",
        "Posti letto Day Surgery",
        "Totale posti letto",
    ]

    # Retrieve and read file
    posti_letto = pd.DataFrame(download_salutegov_csv(url_posti_letto))

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

    print(posti_letto)
    posti_letto.info(verbose=1)

    return posti_letto


@cli.command(name="prep_from_salutegovit")
@click.option(
    "--out_fp", default="./data/prepped/istat/2010-2019_posti_letto_by_province.csv"
)
def posti_letto_to_csv(out_fp):
    posti_letto = posti_letto_from_salutegov()
    posti_letto.to_csv(out_fp, index=False)


cli.add_command(posti_letto_to_csv)

if __name__ == "__main__":
    cli()
