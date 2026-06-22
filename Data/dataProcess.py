import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from API import requisitions as req
import pandas as pd
import json

#data precisa de ser no formato AAAA-MM-DD

def occurrencesProcessed(scientificName, startDate=None, endDate=None):
    occurrence = req.getOccurrence(scientificName,startDate,endDate)
    df = pd.DataFrame(occurrence["results"])
    cols = ["basisOfRecord", "date_year", "institutionCode", "locality", "vernacularName", "bathymetry", "shoredistance", "decimalLatitude", "decimalLongitude"]
    df = df.reindex(columns=cols)
    return df


if __name__ == "__main__":
    req = occurrencesProcessed("Rhincodon typus")
    with open("./API/output.json", "w", encoding="utf-8") as f:
         f.write(req.to_json(orient="records", indent=4, force_ascii=False))