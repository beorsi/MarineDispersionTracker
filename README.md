# Marine Dispersion Tracker

A desktop application for tracking and visualizing the global dispersion of marine species using real occurrence data from the Ocean Biodiversity Information System (OBIS).

## Overview

Marine Dispersion Tracker fetches live data from the OBIS API and presents it through an interactive interface, allowing users to explore where marine species have been recorded across the world's oceans.

## Features

- **Interactive world map** displaying the 1,000 most recent occurrence records for the selected species
- **Species statistics card** showing total OBIS records, year range, average depth, average shore distance, most common locality, and record type breakdown
- **10 tracked species** including whales, sharks, and reef fish
- **Real-time data loading** with async fetching and loading indicators

## Tracked Species

| Common Name | Scientific Name |
|---|---|
| Sperm whale | *Physeter macrocephalus* |
| Whale shark | *Rhincodon typus* |
| Great white shark | *Carcharodon carcharias* |
| Blue whale | *Balaenoptera musculus* |
| Hammerhead shark | *Sphyrna zygaena* |
| Thresher shark | *Alopias vulpinus* |
| Killer whale | *Orcinus orca* |
| Humpback whale | *Megaptera novaeangliae* |
| Shortfin mako | *Isurus oxyrinchus* |
| Blacktip reef shark | *Carcharhinus melanopterus* |

## Tech Stack

- **Python** — core language
- **Flet 0.86.4** — desktop UI framework
- **flet-map 0.86.4** — interactive map component
- **pandas** — data processing
- **OBIS API v3** — occurrence data source (`https://api.obis.org/v3/`)

## Project Structure

```
MarineDispersionTracker/
├── API/
│   └── requisitions.py       # OBIS API calls
├── Data/
│   ├── dataProcess.py        # Data fetching and processing
│   └── species.py            # Species registry
├── UI/
│   ├── sidebar.py            # Species selection sidebar
│   ├── speciesCard.py        # Statistics card
│   └── speciesMap.py         # Interactive map + legend + image
├── assets/
│   ├── fonts/
│   └── images/
└── main.py                   # App entry point
```

## Requirements

```
flet==0.86.4
flet-map==0.86.4
flet-desktop==0.86.4
flet-cli==0.86.4
pandas
requests
```

## Data Source

All occurrence data is sourced from [OBIS (Ocean Biodiversity Information System)](https://obis.org), a global open-access repository for marine biodiversity data.
