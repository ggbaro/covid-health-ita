import click
import os
import pandas as pd
from ..transcoding.names.ita import col, var
from ..transcoding.metadata import dtype
from ..utils import convert_dtype


url_istat = "http://dati.istat.it/DownloadFiles.aspx?&DatasetCode={}&Lang=IT"

figures = {
    "death_causes": "DCIS_CMORTE1_RES"
}

internal_data = {
    "death_by_cause": "https://raw.githubusercontent.com/ggbaro/covid-health-ita/master/data/external/istat_DCIS_CMORTE1_EV_20200322.csv",
}

def parse_istat_dataset(df, col=col, dtype=dtype):
    if df in internal_data.keys():
        df = internal_data[df]

    if isinstance(df, str):
        df = pd.read_csv(df, dtype={"Codice Comune": str}, parse_dates=['TIME'])

    df = df.rename(columns=col['istat'])
    
    for column, old, new in var["istat"]:
        if column in df.columns:
            df[column] = df[column].str.replace(old, new)
            

    # for column in df.columns:
    #     df = df.loc[df[column] != "total"]

    # filter specified columns
    df = df.loc[:, set(col['istat'].values()).intersection(df.columns)] 
    
    print(df)

    # df = convert_dtype(df, dtype)

    return df


# --- CLI ---


@click.group()
def cli():
    pass


@click.command(
    name="from-csv",
    help="Provide `source`, a file path or internal data shortcut "
        f"(one of {list(internal_data.keys())}).")
@click.argument("source")
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
