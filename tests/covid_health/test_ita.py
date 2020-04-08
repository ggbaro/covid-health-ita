import pytest
import pandas as pd
from covid_health.ita import (
    prep_istat,
    prep_salutegov,
    prep_other_data,
    prep_pcm_dpc,
)

# ISTAT
@pytest.mark.parametrize(
    "figure", ["2019_pop_regions", "2018_pop_regions", "2019_pop_provinces"],
)
def test_istat_geodemo(figure):
    result = prep_istat.parse_istat_geodemo(figure)
    assert isinstance(result, pd.DataFrame)
    assert result.shape[1] > 1
    print(result.columns)


def test_parse_istat_daily_deaths():
    result = prep_istat.parse_daily_deaths()
    assert isinstance(result, tuple)
    assert isinstance(result[0], pd.DataFrame)
    assert isinstance(result[1], tuple)
    assert isinstance(result[1][0], pd.Series)
    assert result[0].shape[1] > 1
    print(result[0].columns)


# SALUTE GOV
@pytest.mark.parametrize(
    "figure",
    [
        "hospital_beds_by_discipline_hospital",
        "asl_expenditure_by_device_2014",
        "asl_expenditure_by_device_2015",
        "asl_expenditure_by_device_2016",
        "asl_expenditure_by_device_2017",
        "asl_comuni_pop",
    ],
)
def test_salutegov(figure):
    result = prep_salutegov.parse_dataset(figure, verbose=1)
    assert isinstance(result, pd.DataFrame)
    assert result.shape[1] > 1
    print(result.columns)


def test_salutegov_missingfigure():
    with pytest.raises(NotImplementedError):
        prep_salutegov.parse_dataset("non-existing-figure", verbose=1)


# DPC
@pytest.mark.parametrize(
    "figure", ["dpc-regions", "dpc-province",],
)
def test_dpc(figure):
    result = prep_pcm_dpc.parse_covid_data(figure)
    assert isinstance(result, pd.DataFrame)
    assert result.shape[1] > 1
    print(result.columns)


def test_dpc_missingfigure():
    with pytest.raises(NotImplementedError):
        prep_pcm_dpc.parse_covid_data("non-existing-figure")
