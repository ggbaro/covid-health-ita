import os
import click
import pandas as pd

elenco_codici_denominazioni_comuni_20200101 = (
    "https://raw.githubusercontent.com/"
    "ondata/covid19italia/master/risorse/"
    "Elenco-codici-statistici-e-denominazioni-al-01_01_2020.csv"
)

elenco_comuni_col_names = {
    "Codice Regione": "region_code",
    "Codice dell'Unità territoriale sovracomunale (valida a fini statistici)": "territorial_unit_stat_code",
    "Codice Provincia (Storico)(1)": "prov_code_hist",
    "Progressivo del Comune (2)": "town_prog_id",
    "Codice Comune formato alfanumerico": "zip_code",
    "Denominazione in italiano": "town",
    "Ripartizione geografica": "geo_partition",
    "Denominazione regione": "region",
    "Denominazione dell'Unità territoriale sovracomunale (valida a fini statistici)": "province",
    "Flag Comune capoluogo di provincia/città metropolitana/libero consorzio": "is_province",
    "Sigla automobilistica": "province_short",
    "Popolazione legale 2011 (09/10/2011)": "population_2011",
    "NUTS1": "NUTS1",
    "NUTS2(3)": "NUTS2",
    "NUTS3": " NUTS3",
}

dtypes = {
    "Codice Comune formato alfanumerico": str,
}


def parse_elenco_comuni(csv_url=elenco_codici_denominazioni_comuni_20200101):
    df = pd.read_csv(csv_url, dtype=dtypes)
    df = df.loc[:, elenco_comuni_col_names.keys()]
    df = df.rename(columns=elenco_comuni_col_names)

    # small bug
    df = df.loc[df.province != "Trentino Alto Adige / Südtirol"]
    # fix province names
    df.loc[df.province == "Valle d'Aosta/Vallée d'Aoste", "province"] = "Aosta"
    df.loc[df.province == "Bolzano/Bozen", "province"] = "Bolzano"
    # df.loc[df.province == "Massa-Carrara", "province"1f] = "Massa Carrara"

    return df


# --- CLI ---


@click.group()
def cli():
    pass


@click.command(
    name="comuni-from-github",
    help="sourced from https://github.com/ondata/covid19italia",
)
@click.option("--out_fp", default="./data/interim/istat/2020_denominazione_comuni.csv")
@click.option("--csv-url", default=elenco_codici_denominazioni_comuni_20200101)
def parse_git_ondata(out_fp, csv_url):
    data = parse_elenco_comuni(elenco_codici_denominazioni_comuni_20200101)
    os.makedirs(os.path.dirname(out_fp), exist_ok=True)
    data.to_csv(out_fp, index=False)


cli.add_command(parse_git_ondata)


if __name__ == "__main__":
    cli()
