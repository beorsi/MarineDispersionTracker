import requests as rq
import json

url = "https://api.obis.org/v3/"

def getTaxon(scientificName):
    response = rq.get(url + "taxon/" + scientificName)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("There has been an error while fetching the data")
        return


def getOccurrence(scientificName, startDate=None, endDate=None, size=1000):

    params = {"scientificname": scientificName, "size": size, "sort":"date_end", "dir":"desc"}
    
    if startDate:
        params["startdate"] = startDate
    if endDate:
        params["enddate"] = endDate
    
    response = rq.get(url + "occurrence", params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("There has been an error while fetching the data")
        return

def getCoordinates(scientificName, startDate=None, endDate=None):
    params = {"scientificname": scientificName}
    
    if startDate:
        params["startdate"] = startDate
    if endDate:
        params["enddate"] = endDate
    
    response = rq.get(url + "occurrence/points", params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("There has been an error while fetching the data")
        return

#dev Only
def getDatabankInfo(scientificName):
    params = {"scientificname": scientificName}

    response = rq.get(url + "statistics", params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("There has been an error while fetching the data")
        return

if __name__ == "__main__":
    req = getTaxon("Rhincodon typus")
    
    with open("./API/output.json", "w", encoding="utf-8") as f:
        json.dump(req, f, indent=4, ensure_ascii=False)