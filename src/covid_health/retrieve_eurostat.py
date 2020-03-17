import eurostat
from .transcoding.names.eurostat import col, var
from .utils import parse_panel

figures = {
    "population-NUTS3": "demo_r_pjangrp3"
}


def parse_eurostat(
    figure,
    value_name="value",
    col=col,
    val=val,
):
    df =  eurostat.get_data_df(figures[figure])
    df = parse_panel(df)

    return df

