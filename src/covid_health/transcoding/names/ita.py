col = {
    'dpc-province': {
        # dpc province
        'codice_provincia': 'province_code',
        'codice_regione': 'region_code',
        'data': 'date',
        'denominazione_provincia': 'province',
        'denominazione_regione': 'region',
        'lat': 'latitude',
        'long': 'longitude',
        'sigla_provincia': 'province_short',
        'stato': 'country',
        'totale_casi': 'tot_n_cases',
    },
    'dpc-regions': {
        # dpc regions
        'deceduti': 'n_deceased',
        'dimessi_guariti': 'n_discharged_recovered',
        'isolamento_domiciliare': 'n_home_quarantine',
        'nuovi_attualmente_positivi': 'n_new_cases',
        'ricoverati_con_sintomi': 'n_hospitalized',
        'tamponi': 'n_tested',
        'terapia_intensiva': 'n_intensive_care',
        'totale_attualmente_positivi': 'n_active_cases',
        'totale_ospedalizzati': 'tot_n_hospitalized',
    },

    "hospital_beds_by_discipline_hospital": {
        # salute.gov.it/dataset_96 hospital_beds_by_discipline_hospital
        "Anno": "year",
        "Codice Regione": "region_code",
        "Descrizione Regione": "region",
        "Codice Azienda": "asl_code",
        "Tipo Azienda": "asl_type",
        "Codice struttura": "hospital_id",
        "Subcodice": "subcode",
        "Denominazione Struttura/Stabilimento": "hospital_name",
        "Indirizzo": "address",
        "Codice Comune": "zip_code",
        "Comune": "town",
        "Sigla Provincia": "province_short",
        "Codice tipo struttura": "hospital_type_id",
        "Descrizione tipo struttura": "hospital_type",
        "Codice disciplina": "discipline_id",
        "Descrizione disciplina": "discipline",
        "Tipo di Disciplina": "discipline_type",
        "N° Reparti": "n_wards",
        "Posti letto degenza ordinaria": "n_hosp_bed_ordinary",
        "Posti letto degenza a pagamento": "n_hosp_bed_paid",
        "Posti letto Day Hospital": "n_hospital_bed_dayhospital",
        "Posti letto Day Surgery": "n_hospital_bed_daysurgery",
        "Totale posti letto": "tot_n_hospital_bed",
    },
    "salutegov-2": {
        # salute.gov.it/dataset_96 posti letto disciplina
        'ANNO': "year",
        'CODICE REGIONE': "region_code",
        'DENOMINAZIONE REGIONE': "region",
        'CODICE AZIENDA': "asl_code",
        'DENOMINAZIONE AZIENDA': "asl_name",
        'INDIRIZZO': "address",
        'CAP': "zip_code",
        'COMUNE': "town",
        'SIGLA PROVINCIA': "province_short",
        'TELEFONO': "phone",
        'FAX': "fax",
        'E-MAIL': "email",
        'SITO WEB': "website",
        'PARTITA IVA': "vat",
    },
    'istat': {
        # Istat population by province, gender, age
        "ITTER107": "NUTS",
        "TIPO_DATO15": "data_type",
        "ETA1": "age_id",
        "STATCIV2": "marital_status_id",
        "SEXISTAT1": "gender_id",
        "Territory": "province",
        "Gender": "gender",
        "Age": "age",
        "Marital status": "marital_status",
        "Value": "value",
        "TIME": "time",
    }

}


var = {
    "istat": [
        ("province", "Valle d'Aosta / Vallée d'Aoste", "Aosta"),
        ("province", "Bolzano / Bozen", "Bolzano"),
        ("province", "Massa-Carrara", "Massa Carrara"),
        ("genders", "males", "male"),
        ("genders", "females", "female"),
        ("age", "[A-z ]+", ""),
    ]
}