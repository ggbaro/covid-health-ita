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
  eurostat
  ita
  worldometers  choose figure between ['age_sex_demographics', 'countries']
```

Every data source has its own sub-command

```bash
$ covid-data eurostat --help
Usage: covid-data eurostat [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  from-eurostat  one of ['demo_r_d2jan', 'demo_r_pjangrp3',
                 'demo_r_d3dens',...

  list-datasets  List available datasets
```

For Eurostat and other sources, there are help functions such as `list-datasets`:

```bash
$ covid-data eurostat list-datasets
[0] demo_r_d2jan -> Population on 1 January by age, sex and NUTS 2 region
[1] demo_r_pjangrp3 -> Population on 1 January by age group, sex and NUTS 3 region
...
[5] hlth_sha11_hf -> Health care expenditure by financing scheme
[69] hlth_ehis_hc6 -> Self-reported consultation of a psychologist or physiotherapist by sex, age and educational attainment level (%)
```

You can build your datset locally in no time:

```bash
$ covid-data eurostat from-eurostat --ext .csv.gz demo_r_d2jan
saving to:  ./data/interim/eurostat/demo_r_d2jan.csv.gz
         NUTS    unit  gender     age  year population
0          AL  number  female   TOTAL  2010   1459025 
1         AL0  number  female   TOTAL  2010   1459025 
2        AL01  number  female   TOTAL  2010           
3        AL02  number  female   TOTAL  2010           
4        AL03  number  female   TOTAL  2010           
...       ...     ...     ...     ...   ...        ...
5090845  UKM7  number   total  Y_OPEN  2016       342 
5090846  UKM8  number   total  Y_OPEN  2016       231 
5090847  UKM9  number   total  Y_OPEN  2016       164 
5090848   UKN  number   total  Y_OPEN  2016       274 
5090849  UKN0  number   total  Y_OPEN  2016       274 

[5090850 rows x 6 columns]
```

Data Sources
------------

#### World

| Category          | Name      | Type             | URL                  | cli |
|-------------------|-----------|------------------|----------------------|-----|
| Unofficial Web Source  | Worldometer  | Covid19 | [worldometers.info](https://www.worldometers.info/) | `$ covid-data worldometers` |

#### Europe

| Category          | Name      | Type             | URL                  | cli |
|-------------------|-----------|------------------|----------------------|-----|
| Institutional DB  | Eurostat  | Open Data | [ec.europa.eu/eurostat](https://ec.europa.eu/eurostat) | `$ covid-data eurostat` |

#### Italy

Submodule `covid_health.ita`
| Category          | Name      | Type      | URL                  | cli |
|-------------------|-----------|-----------|----------------------|-----|
| Insititutional DB | Istat     | Open Data | [dati.istat.it](http://dati.istat.it/) | `$ covid-data ita istat` |
| Institutional DB | Open Data della Pubblica Amministrazione Italiana - AGID | Health Open Data | [dati.gov.it](https://www.dati.gov.it/content/italian-open-data-license-v20) | `$ covid-data ita salute-gov` |
| Official Git Repo | Protezione Civile - COVID-19  | COVID-19 Data | [github.com/pcm-dpc/COVID-19](https://github.com/pcm-dpc/COVID-19) | `$ ` |
| Unofficial Git Repo | Covid19italia  | COVID-19 Data | [github.com/ondata/covid19italia](https://github.com/ondata/covid19italia) | `$ ` |


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
