import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from API import requisitions as req
import pandas as pd

#data precisa de ser no formato AAAA-MM-DD

def occurrencesProcessed(scientificName, startDate=None, endDate=None):
    occurrence = req.getOccurrence(scientificName, startDate, endDate)
    df = pd.DataFrame(occurrence["results"])
    cols = ["basisOfRecord", "date_year", "institutionCode", "locality", "vernacularName", "bathymetry", "shoredistance", "decimalLatitude", "decimalLongitude"]
    df = df.reindex(columns=cols)
    return df, occurrence.get("total", len(df))


def getSpeciesStats(scientificName):
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=2) as executor:
        f_occurrence = executor.submit(req.getOccurrence, scientificName)
        f_stats = executor.submit(req.getDatabankInfo, scientificName)
        occurrence = f_occurrence.result()
        stats_raw = f_stats.result()

    df = pd.DataFrame(occurrence["results"])
    cols = ["basisOfRecord", "date_year", "institutionCode", "locality", "vernacularName", "bathymetry", "shoredistance", "decimalLatitude", "decimalLongitude"]
    df = df.reindex(columns=cols)

    total_real = stats_raw.get("records", len(df))
    avg_depth = round(df["bathymetry"].dropna().mean(), 1) if not df["bathymetry"].dropna().empty else None
    avg_shore = round(df["shoredistance"].dropna().mean() / 1000, 1) if not df["shoredistance"].dropna().empty else None
    years = df["date_year"].dropna()
    last_year = int(years.max()) if not years.empty else None
    first_year = int(years.min()) if not years.empty else None
    top_locality = df["locality"].dropna()
    top_locality = top_locality[top_locality.str.contains(r'[A-Za-z]{5,}', regex=True)]
    top_locality = top_locality.mode()
    top_locality = top_locality.iloc[0] if not top_locality.empty else None
    VALID_RECORD_TYPES = {"HumanObservation", "MachineObservation", "PreservedSpecimen", "MaterialSample", "Occurrence"}
    normalize_map = {v.lower().replace("_", ""): v for v in VALID_RECORD_TYPES}
    record_types_series = df["basisOfRecord"].dropna()
    record_types_series = record_types_series.str.strip().str.lower().str.replace("_", "", regex=False)
    record_types_series = record_types_series.map(normalize_map)
    record_types_series = record_types_series.dropna()
    record_counts = record_types_series.value_counts()
    return {
        "total": total_real,
        "avg_depth_m": avg_depth,
        "avg_shore_km": avg_shore,
        "last_occurrence": last_year,
        "first_occurrence": first_year,
        "top_locality": top_locality,
        "record_types": record_counts.to_dict(),
    }


if __name__ == "__main__":
    import json
    result, _ = occurrencesProcessed("Rhincodon typus")
    with open("./API/output.json", "w", encoding="utf-8") as f:
        f.write(result.to_json(orient="records", indent=4, force_ascii=False))
