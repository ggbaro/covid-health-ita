import csv
import gzip
import os

import click
import pandas as pd
import numpy as np
import requests

from .transcoding.names.eurostat import col, var
from .transcoding.metadata import dtype
from .utils import download_and_parse_gzip_csv

eurostat_gz_url = (
    "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing"
)

datasets = {
    # POPULATION
    "demo_r_d2jan": "Population on 1 January by age, sex and NUTS 2 region",
    "demo_r_pjangrp3": "Population on 1 January by age group, sex and NUTS 3 region",
    "demo_r_d3dens": "Population density by NUTS 3 region",
    # HEALTH CARE EXPENDITURE
    "hlth_sha11_hp": "Health care expenditure by provider",
    "hlth_sha11_hc": "Health care expenditure by function",
    "hlth_sha11_hf": "Health care expenditure by financing scheme",
    "hlth_sha11_hchp": "Expenditure for selected health care functions by health care providers",
    "hlth_sha11_hchf": "Expenditure for selected health care functions by health care financing schemes",
    "hlth_sha11_hphf": "Expenditure for selected health care providers by health care financing schemes",
    # HEALTH CARE PERSONNEL
    "hlth_rs_prshp1": "Health personnel employed in hospital",
    "hlth_rs_prsns": "Nursing and caring professionals",
    "hlth_rs_spec": "Physicians by medical speciality",
    "hlth_rs_phys": "Physicians by sex and age",
    "hlth_rs_prsrg": "Health personnel by NUTS 2 regions",
    "hlth_rs_grd": "Health graduates",
    "hlth_rs_prs1": "Health personnel (excluding nursing and caring professionals)",
    "hlth_rs_wkmg": "Health workforce migration",
    # HEALTH CARE CAPACITY
    "hlth_rs_bds": "Hospital beds by type of care",
    "hlth_rs_bds2": "Hospital beds by hospital ownership",
    "hlth_rs_bdsrg": "Hospital beds by NUTS 2 regions",
    "hlth_rs_bdsns": "Long-term care beds in nursing and residential care facilities by NUTS 2 regions",
    "hlth_rs_tech": "Technical resources in hospital",
    "hlth_rs_equip": "Medical technology",
    # HOSPITALIZATION AND DIAGNOSES
    "hlth_co_dischls": "Hosp. discharges and length of stay for inpatient and curative care",
    "hlth_co_bedoc": "Curative care bed occupancy rate",
    "hlth_co_dischnr": "Non-residents among all hosp. discharges, %",
    "hlth_ehis_ho1e": "Self-reported hospital in-patient and day-patient admissions by sex, age and educational attainment level",
    "hlth_ehis_ho1u": "Self-reported hospital in-patient and day-patient admissions by sex, age and degree of urbanisation",
    "hlth_co_disch1": "Hosp. discharges by diagnosis, in-patients, tot number",
    "hlth_co_disch2": "Hosp. discharges by diagnosis, in-patients, per 100 000 inhabitants",
    "hlth_co_disch3": "Hosp. discharges by diagnosis, day cases, tot number",
    "hlth_co_disch4": "Hosp. discharges by diagnosis, day cases, per 100 000 inhabitants",
    "hlth_ehis_hc8": "Self-reported hospital in-patient and day-patient admissions by sex, age and educational attainment level (%)",
    "hlth_co_disch1t": "Hosp. discharges by diagnosis and NUTS 2 regions, in-patients, tot number - tot",
    "hlth_co_disch1m": "Hosp. discharges by diagnosis and NUTS 2 regions, in-patients, tot number - males",
    "hlth_co_disch1f": "Hosp. discharges by diagnosis, NUTS 2 regions, in-patients and tot number - females",
    "hlth_co_disch2t": "Hosp. discharges by diagnosis and NUTS 2 regions, in-patients, per 100 000 inhabitants - tot",
    "hlth_co_disch2m": "Hosp. discharges by diagnosis and NUTS 2 regions, in-patients, per 100 000 inhabitants - males",
    "hlth_co_disch2f": "Hosp. discharges by diagnosis and NUTS 2 regions, in-patients, per 100 000 inhabitants - females",
    "hlth_co_disch3t": "Hosp. discharges by diagnosis and NUTS 2 regions, day cases, tot number - tot",
    "hlth_co_disch3m": "Hosp. discharges by diagnosis and NUTS 2 regions, day cases, tot number - males",
    "hlth_co_disch3f": "Hosp. discharges by diagnosis and NUTS 2 regions, day cases, tot number - females",
    "hlth_co_disch4t": "Hosp. discharges by diagnosis and NUTS 2 regions, day cases, per 100 000 inhabitants - tot",
    "hlth_co_disch4m": "Hosp. discharges by diagnosis and NUTS 2 regions, day cases, per 100 000 inhabitants - males",
    "hlth_co_disch4f": "Hosp. discharges by diagnosis and NUTS 2 regions, day cases, per 100 000 inhabitants - females",
    "hlth_co_inpst": "In-patient average length of stay (days)",
    "hlth_co_inpstt": "In-patient average length of stay (days) by NUTS 2 regions - tot",
    "hlth_co_inpstm": "In-patient average length of stay (days) by NUTS 2 regions - males",
    "hlth_co_inpstf": "In-patient average length of stay (days) by NUTS 2 regions - females",
    "hlth_co_hosday": "Hospital days of in-patients",
    "hlth_co_hosdayt": "Hospital days of in-patients by NUTS 2 regions - tot",
    "hlth_co_hosdaym": "Hospital days of in-patients by NUTS 2 regions - males",
    "hlth_co_hosdayf": "Hospital days of in-patients by NUTS 2 regions - females",
    "hlth_co_proc2": "Surgical operations and procedures performed in hospitals by ICD-9-CM",
    "hlth_co_exam": "Medical technologies - examinations by medical imaging techniques (CT, MRI and PET)",
    "hlth_co_ren": "End-stage renal failure (ESRF) patients",
    # MEDICAL CONSULTATIONS
    "hlth_ehis_am1e": "Self-reported time elapsed since last visit to a medical professional by sex, age and educational attainment level",
    "hlth_ehis_am2u": "Self-reported consultations of a medical professional by sex, age and degree of urbanisation",
    "hlth_ehis_am1u": "Self-reported time elapsed since last visit to a medical professional by sex, age and degree of urbanisation",
    "hlth_ehis_am2e": "Self-reported consultations of a medical professional by sex, age and educational attainment level",
    "hlth_ehis_am6e": "Self-reported consultation of mental healthcare or rehabilitative care professionals by sex, age and educational attainment level",
    "hlth_ehis_am6u": "Self-reported consultation of mental healthcare or rehabilitative care professionals by sex, age and degree of urbanisation",
    "hlth_hc_phys": "Consultation of a medical doctor (in private practice or as outpatient) per inhabitant",
    "hlth_hc_dent": "Consultation of a dentist per inhabitant",
    "hlth_ehis_am2b": "Self-reported consultations of a medical professional by sex, age and country of birth",
    "hlth_ehis_am2c": "Self-reported consultations of a medical professional by sex, age and country of citizenship",
    "hlth_ehis_am2d": "Self-reported consultations of a medical professional by sex, age and level of activity limitation",
    "hlth_ehis_am6d": "Self-reported consultation of mental healthcare or rehabilitative care professionals by sex, age and level of activity limitation",
    "hlth_ehis_hc5": "Self-reported consultation of a medical professional by sex, age and educational attainment level (%)",
    "hlth_ehis_hc6": "Self-reported consultation of a psychologist or physiotherapist by sex, age and educational attainment level (%)",
}


def parse_eurostat_dataset(dataset_id, dtype=dtype, col=col):
    data = download_and_parse_gzip_csv(
        eurostat_gz_url, params={"file": f"data/{dataset_id}.tsv.gz"}
    )
    data = pd.DataFrame(data)
    data.columns = [col.strip() for col in data.columns]
    data = data.replace(":", "").replace(": ", "")
    data = data.rename(columns={r"geo\time": "geo"})

    time_cols = set(data.filter(regex="[1-2][0-9]{3}").columns)
    other_cols = set(data.columns).difference(time_cols)

    data = data.melt(
        id_vars=other_cols, value_vars=time_cols, var_name="time", value_name="value",
    )

    data = data.rename(columns=col["eurostat"])

    # dtype = {k: v for k, v in dtype.items() if k in data.columns}
    # data = data.astype(dtype)

    print(data)

    return data


def list_eurostat_datasets():
    for ix, (dataset_id, descr) in enumerate(datasets.items()):
        # descr_split = []  # IN CASE WE WANT TO SPLIT LINES
        # row = ""
        # for n, word in enumerate(descr.split(" ")):
        #     if len(f"{row} {word}") > 109:
        #         descr_split.append(row)
        #         row = ""
        #     row += f" {word}"
        # descr_split.append(row)
        # descr = "\n    ".join(descr_split)
        print(f"[{ix}] {dataset_id} -> {descr}")


# --- CLI ---


@click.group(help="Datasets creation from Eurostat.")
def cli():
    pass


@cli.command(name="list-datasets", help="List available datasets")
def list_datasets():
    list_eurostat_datasets()


@cli.command(name="from-eurostat", help="one of {}".format(list(datasets.keys())))
@click.argument("dataset_id")
@click.option(
    "--out-fp",
    help="if not specified, defaults to 'dataset_id.csv'",
    default="./data/interim/eurostat/",
)
@click.option(
    "--ext",
    help="if no --out-fp specified, determines output format. "
    "Allowed are `['.csv', '.csv.gz', '.csv.zip']`.",
    default=".csv",
)
def eurostat_to_csv(dataset_id, out_fp, ext):

    if np.all(
        [
            ext not in out_fp.rsplit("/", 1)[-1]
            for ext in (".csv", ".csv.gz", ".csv.zip")
        ]
    ):
        out_fp = os.path.join(out_fp, dataset_id + ext)
    os.makedirs(os.path.dirname(out_fp), exist_ok=True)

    print("saving to: ", out_fp)

    data = parse_eurostat_dataset(dataset_id)
    data.to_csv(out_fp, index=False)


cli.add_command(eurostat_to_csv)
cli.add_command(list_datasets)


if __name__ == "__main__":
    cli()
