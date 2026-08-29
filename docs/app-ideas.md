# Bangladesh App Ideas — Life-Saving + Data Science

Notes from brainstorming. Filter used: a real life-saving problem in Bangladesh,
a genuine data-science component (a partner data scientist owns the model), and
something buildable by me (app + infra).

## 1. Dengue outbreak early-warning app

- **Problem:** Dengue outbreaks hit Dhaka hard every year and often catch hospitals off guard.
- **Data science:** Predict outbreak hotspots from historical case data, rainfall, and temperature patterns.
- **My part:** Live risk map by area + push alerts ("dengue risk rising in your neighborhood — clear standing water, use nets").

## 2. Flood / river-level early-warning system

- **Problem:** Floods are predictable days in advance from upstream river-gauge and rainfall data, but the information doesn't reach the people who need it.
- **Data science:** Model flood risk by region.
- **My part:** SMS/app alert layer for rural users who may not have reliable internet.

## 3. Road accident black-spot alert app

- **Problem:** Bangladesh has one of the world's worst road-safety records.
- **Data science:** Analyze accident location data (news reports, police data where available) to flag dangerous stretches and times.
- **My part:** Warn drivers approaching a known black spot — similar to speed-camera apps.

## 4. Air-quality health-risk alerts for vulnerable groups

- **Problem:** Dhaka's AQI is frequently hazardous.
- **Data science:** Predict pollution spikes and personalize risk (asthma, elderly, kids) instead of showing a generic AQI number.
- **My part:** Notification / app layer.

## Shared structure

All four split the same way:

- Data scientist owns the prediction model.
- I own the app and infrastructure (my strength).
- Problem discovery — figuring out which one is most urgent right now — is what
  this scraper (problem-radar-app) is already built to surface.

## Next step

Point the scraper at health and disaster news specifically to validate demand
before committing to one idea.

Open question: which direction — health, disaster/flood, or road safety?

## Data sources

Catalogued in [`data/sources/datasets.csv`](../data/sources/datasets.csv) and
[`datasets.json`](../data/sources/datasets.json) — 18 sources across the four
ideas, with coverage, format, access route and license for each. See
[`data/README.md`](../data/README.md) for the columns and the fetcher.

Highlights per idea:

- **Dengue** — OpenDengue (case counts since 1990, 102 countries) for history,
  HealthMap for near-real-time signal ahead of official counts, DGHS daily press
  releases as national ground truth.
- **Flood** — Google Flood Hub (7-day forecasts, launched in Bangladesh) and its
  Flood Forecasting API for consuming forecasts directly; Inundation History
  (1999–2020) and GRRR (1980–2023) if we train our own; FFWC gauges and GloFAS as
  independent checks.
- **Road safety** — the 2025 figshare dataset integrating ARI (BUET), BRTA, DMP
  and Military Police records with field data (2007–2024); the IEEE DataPort
  newspaper-derived set (2016–2019); this scraper to extend the media angle past
  2019.
- **Air quality** — OpenAQ REST API and WAQI/aqicn (free keys, fastest to stand
  up), IQAir for paid forecasts, CAMS and DoE CASE for cross-checks.

Official Bangladesh figures undercount: WHO put 2021 road deaths near 32,000
against roughly 11,000 officially — near a 3x gap. Each idea therefore pairs a
national source with an independent or international one.

Lowest-friction prototype: **flood**. The forecasting work is already done and
Bangladesh-proven (Google + IRC anticipatory cash-relief pilots), so the build is
mostly the alert and distribution layer — the part that plays to my strength.
