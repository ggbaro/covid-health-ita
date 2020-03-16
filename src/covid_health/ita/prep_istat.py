import click
import os
import pandas as pd
from ..transcoding.names.ita import col, var
from ..transcoding.metadata import dtype
from ..utils import convert_dtype


def parse_istat_dataset(df, col=col, dtype=dtype):
    if isinstance(df, str):
        df = pd.read_csv(df, dtype={"Codice Comune": str})

    df = df.rename(columns=col['istat'])
    
    for column, old, new in var["istat"]:
        if column in df.columns:
            df[column] = df[column].str.replace(old, new)
            

    for column in df.columns:
        df = df.loc[df[column] != "total"]
        
    # filter specified columns
    df = df.filter(set(col['istat'].values()).intersection(set(df.columns)))
    
    print(df)

    # df = convert_dtype(df, dtype)

    return df


# --- CLI ---


@click.group()
def cli():
    pass


@click.command(name="from-csv")
@click.argument("source_csv_fp")
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
