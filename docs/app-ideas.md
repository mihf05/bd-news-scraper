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
