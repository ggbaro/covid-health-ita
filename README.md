Covid-Health
============
_A [Buildnn](http://www.buildnn.com) open source project._

Huge transcoding effort to standardize national and international datasets about COVID-19.



Installation
------------
```bash
$ pip install git+https://github.com/ggbaro/covid-health-ita.git
```

Basic Usage
-----------
Build locally your own data sets for Coronavirus situational awareness using the command line tool `covid-data`.
```bash
$ covid-data
Usage: covid-data [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  eurostat      one of ['hospital_beds_nuts2',...
  ita
  worldometers  choose figure between ['age_sex_demographics', 'countries']
```

```bash
$ covid-data eurostat hospital_beds_nuts2
saving to:  ./data/interim/eurostat/hospital_beds_nuts2.csv
```

Data Sources
------------

#### World
> | Category          | Name      | Type             | URL                  | cli |
> |-------------------|-----------|------------------|----------------------|-----|
> | Unofficial Web Source  | Worldometer  | Covid19 | [worldometers.info](https://www.worldometers.info/) | `$ covid-data worldometers` |

#### Europe
> | Category          | Name      | Type             | URL                  | cli |
> |-------------------|-----------|------------------|----------------------|-----|
> | Institutional DB  | Eurostat  | Open Data | [ec.europa.eu/eurostat](https://ec.europa.eu/eurostat) | `$ covid-data eurostat` |

#### Italy
Submodule `covid_health.ita`
> | Category          | Name      | Type      | URL                  | cli |
> |-------------------|-----------|-----------|----------------------|-----|
> | Insititutional DB | Istat     | Open Data | [dati.istat.it](http://dati.istat.it/) | `$ covid-data ita istat` |
> | Institutional DB | Open Data della Pubblica Amministrazione Italiana - AGID | Health Open Data | [dati.gov.it](https://www.dati.gov.it/content/italian-open-data-license-v20) | `$ covid-data ita salute-gov` |
> | Official Git Repo | Protezione Civile - COVID-19  | COVID-19 Data | [github.com/pcm-dpc/COVID-19](https://github.com/pcm-dpc/COVID-19) | `$ ` |
> | Unofficial Git Repo | Covid19italia  | COVID-19 Data | [github.com/ondata/covid19italia](https://github.com/ondata/covid19italia) | `$ ` |


Dimensions
----------



Project Organization
--------------------
```
.
├── data
│   ├── external
│   ├── interim
│   ├── processed
│   └── raw
├── LICENSE
├── MANIFEST.in
├── notebooks
├── README.md
├── requirements-dev.txt
├── requirements.txt
├── setup.py
└── src
    └── covid_health
        ├── cli.py
        ├── __init_.py
        ├── ita
        ├── prep_eurostat.py
        ├── prep_worldometer.py
        ├── retrieve_eurostat.py
        ├── transcoding
        └── utils.py

```
