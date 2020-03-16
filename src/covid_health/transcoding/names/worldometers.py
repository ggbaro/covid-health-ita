col = {
    'age_sex_demographics': {
        # worldometers covid deepdive age
        "AGE": "age",
        "SEX": "gender",
        "PRE-EXISTING CONDITION": "pre_medical_condition",
        "DEATH RATE confirmed cases": "death_rate_confirmed_rel_freq",
        "DEATH RATE all cases": "death_rate_all_rel_freq",
    },
    'countries': {
        # worldometers covid general countries data
        'Country,Other': 'country',
        'TotalCases': 'tot_n_cases',
        'NewCases': 'n_new_cases',
        'TotalDeaths': 'tot_n_deceased',
        'NewDeaths': 'n_new_deceased',
        'TotalRecovered': 'tot_n_recovered',
        'ActiveCases': 'n_active_cases',
        'Serious,Critical': 'n_serious_critical',
        'Tot Cases/1M pop': 'n_cases_per_mln_habitants',
    }
}

val = dict(
    age_sex_demographics=[
        ("gender", "Male", "male"),
        ("gender", "Female", "female"),
        ("death_rate_confirmed_rel_freq", "[A-z\% ]+", ""),
        # ("death_rate_confirmed_rel_freq", "", "0."),
        ("death_rate_all_rel_freq", "[A-z\% ]+", ""),
        #("death_rate_all_rel_freq", "", "0."),
    ],
    countries=[
        ("n_new_cases", ",", ""),
        ("country", ":", ""),
    ],
)