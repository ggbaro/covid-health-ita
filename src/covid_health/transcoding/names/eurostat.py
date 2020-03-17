import requests
import csv
import pandas as pd


class EurostatDict:
    def __init__(self, lang="en"):
        self.url = "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing"
        self.lang = lang

    def __getitem__(self, item):
        response = requests.get(
            self.url, params={"file": f"dic/{self.lang}/{item}.dic"}
        )

        lines = [line.decode().strip() for line in response.iter_lines()]

        if lines[0].startswith("<!DOCTYPE html"):
            raise NotImplementedError(f"The field '{item}' is not a valid field.")
        dic = pd.DataFrame(
            csv.DictReader(
                lines,
                delimiter="\t",
                fieldnames=["code", "human_name"],
            )
        )

        dic = dic.values.tolist()

        return dic


col = {
    "eurostat": {
        "sex": "sex",
        "unit": "unit",
        "age": "age",
        "icd10": "icd10",
        "indic_he": "indic_he",
        "geo": "geo",
        "time": "time",
        "value": "value",
    }
}

var = {
    "eurostat": EurostatDict()
}
