import click
import os
import pandas as pd


@click.group()
def cli():
    pass


def population_df_from_csv(istat_population_csv_fp):
    population_df = pd.read_csv(istat_population_csv_fp)
    return population_df


def parse_data(population_df):
    # small bug
    population_df = population_df.loc[
        population_df.Territory != "Trentino Alto Adige / Südtirol"
    ]
    # fix province names
    population_df.loc[
        population_df.Territory == "Valle d'Aosta / Vallée d'Aoste", "Territory"
    ] = "Aosta"
    population_df.loc[
        population_df.Territory == "Bolzano / Bozen", "Territory"
    ] = "Bolzano"
    population_df.loc[
        population_df.Territory == "Massa-Carrara", "Territory"
    ] = "Massa Carrara"

    # remove totals
    population_df = population_df.loc[population_df.Gender != "total"]
    population_df = population_df.loc[population_df.Age != "total"]
    population_df = population_df.loc[population_df["Marital status"] != "total"]

    # rename to match
    col_names = {
        "Territory": "denominazione_provincia",
        "Gender": "gender",
        "Age": "age",
        "Marital status	": "marital_status",
        "Value": "population_df",
    }
    population_df = population_df.rename(columns=col_names)

    # extract age as number
    population_df.age = population_df.age.str.replace("[A-z ]+", "").astype(int)

    # filter specified columns
    population_df = population_df.filter(col_names.values())

    # add gender util multiplier to create pyramid plot
    population_df["gender_mult"] = [
        -1 if g == "males" else 1 for g in population_df.gender.values
    ]

    return population_df


@click.command(name="from_csv")
@click.argument("source_csv_fp")
@click.option("--out_fp", default="./data/prepped/istat/2019_population_by_province.csv")
def parse_istat_csv(source_csv_fp, out_fp):
    data = population_df_from_csv(source_csv_fp)
    data = parse_data(data)
    os.makedirs(os.path.dirname(out_fp), exist_ok=True)
    data.to_csv(out_fp, index=False)


if __name__ == "__main__":
    cli.add_command(parse_istat_csv)
    cli()
