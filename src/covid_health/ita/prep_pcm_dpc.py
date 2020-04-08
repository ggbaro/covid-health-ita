import click
import pandas as pd
from ..transcoding.names.ita import col
from ..transcoding.metadata import dtype
from ..fn.epidemic import calculate_epidemic_age


figures = {
    "dpc-province": "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv",
    "dpc-regions": "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",
}
col = col
dtype = dtype


def parse_covid_data(figure="dpc-province"):
    if not figure in figures.keys():
        raise NotImplementedError(
            f"Figure '{figure}' not regognized.\nChoose one of {figures.keys()}"
        )
    df = pd.read_csv(figures[figure], parse_dates=["data"])
    df = df.rename(columns=col[figure])
    if "province_code" in df.columns:
        df.loc[df["province"] == "Napoli", "province_short"] = "NA"
    dtype_ = {k: v for k, v in dtype.items() if k in df.columns}
    df = df.astype(dtype_)

    if "province_code" in df.columns:
        df = df.pipe(
            calculate_epidemic_age,
            group_col="province_code",
            time_col="time",
            total_cases_col="tot_n_cases",
            start_treshold=100,
        )
    elif "region_code" in df.columns:
        df = df.pipe(
            calculate_epidemic_age,
            group_col="region_code",
            time_col="time",
            total_cases_col="tot_n_cases",
            start_treshold=100,
        )
    return df
