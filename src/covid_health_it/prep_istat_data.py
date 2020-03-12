import click
import os
import pandas as pd
from .transcoding.names_map import col_names
from .transcoding.metadata import dtype


def population_df_from_csv(istat_population_csv_fp):
    population_df = pd.read_csv(istat_population_csv_fp)
    return population_df


def parse_population_prov(population_df):
    if isinstance(population_df, str):
        population_df = pd.read_csv(population_df)

    population_df = population_df.rename(columns=col_names)

    # small bug
    population_df = population_df.loc[
        population_df["province"] != "Trentino Alto Adige / Südtirol"
    ]
    # fix province names
    population_df.loc[
        population_df["province"] == "Valle d'Aosta / Vallée d'Aoste", "province"
    ] = "Aosta"
    population_df.loc[
        population_df["province"] == "Bolzano / Bozen", "province"
    ] = "Bolzano"
    population_df.loc[
        population_df["province"] == "Massa-Carrara", "province"
    ] = "Massa Carrara"

    # remove totals
    population_df = population_df.loc[population_df["gender"] != "total"]
    population_df = population_df.loc[population_df["age"] != "total"]
    population_df = population_df.loc[population_df["marital_status"] != "total"]

    # rename to match

    # extract age as number
    population_df.age = population_df.age.str.replace("[A-z ]+", "").astype(int)

    # filter specified columns
    population_df = population_df.filter(
        set([col for col in col_names.values() if col in population_df.columns])
    )

    # add gender util multiplier to create pyramid plot
    population_df["gender_mult"] = [
        -1 if g == "males" else 1 for g in population_df.gender.values
    ]

    return population_df


# --- CLI ---


@click.group()
def cli():
    pass


@click.command(name="from_csv")
@click.argument("source_csv_fp")
@click.option(
    "--out_fp", default="./data/interim/istat/2019_population_by_province.csv"
)
def parse_istat_csv(source_csv_fp, out_fp):
    data = population_df_from_csv(source_csv_fp)
    data = parse_population_prov(data)
    os.makedirs(os.path.dirname(out_fp), exist_ok=True)
    data.to_csv(out_fp, index=False)


cli.add_command(parse_istat_csv)


if __name__ == "__main__":
    cli()
