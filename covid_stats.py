from requests import get
from json import dumps

UK_POP = 68_098_857

ENDPOINT = "https://api.coronavirus.data.gov.uk/v1/data"
AREA_TYPE = "overview"
AREA_NAME = "United Kingdom"
DATE = "2021-02-01"

filters = [f"areaType={AREA_TYPE}", f"areaName={AREA_NAME}"]
# filters = [f"areaType={AREA_TYPE}", f"areaName={AREA_NAME}", f"date={DATE}"]

structure = {
    "date": "date",
    "name": "areaName",
    "code": "areaCode",
    "vaccines": {
        "first_dose": {
            "daily": "newPeopleVaccinatedFirstDoseByPublishDate",
            "cumulative": "cumPeopleVaccinatedFirstDoseByPublishDate",
        },
        "second_dose": {
            "daily": "newPeopleVaccinatedSecondDoseByPublishDate",
            "cumulative": "cumPeopleVaccinatedSecondDoseByPublishDate",
        },
    },
}

api_params = {
    "filters": str.join(";", filters),
    "structure": dumps(structure, separators=(",", ":")),
}


response = get(ENDPOINT, params=api_params, timeout=10)

if response.status_code >= 400:
    raise RuntimeError(f"Request failed: { response.text }")

day = response.json()["data"][0]
total_vaccines_first = day["vaccines"]["first_dose"]["cumulative"]
total_vaccines_second = day["vaccines"]["second_dose"]["cumulative"]
first_percentage = (total_vaccines_first / UK_POP) * 100
total_percentage = ((total_vaccines_first + total_vaccines_second) / (UK_POP * 2)) * 100
print(first_percentage)
print(total_percentage)
