# Sunrise & Sunset ETL Pipeline + Dashboard

## Project Overview

This project is an ETL (Extract, Transform, Load) pipeline that retrieves sunrise and sunset data for a user-specified city, processes and transforms the data, validates data quality, and loads the final results into a PostgreSQL database.

It also prepares the data for use in an interactive Dash dashboard for outdoor planning and daylight scheduling.

## Objectives

The application:
- Displays sunrise and sunset times for a city
- Calculates total daylight duration
- Computes time remaining until the next key light event (sunrise, sunset, or twilight)
- Automatically selects today’s or next day’s cycle depending on time of day
- Supports outdoor planning and daylight-dependent scheduling

# How to Run the Project

## 1. Navigate to project folder
```bash
cd path\to\your\project\folder
```

---

## 2. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 3. Create PostgreSQL database
```sql
CREATE DATABASE sunrise_db;
```

---

# Step 1: Run Data Pipeline (ETL)

This script:
- Extracts data (API)
- Transforms it (feature engineering, time calculations)
- Loads it into PostgreSQL

```bash
python main.py
```

### Example Output
```
2026-06-05 20:21:20,280 - INFO - Geocoding attempt 1 for Clarksville, IN

📊 FINAL DATA
{
  'city': 'Clarksville, IN',
  'sunrise': '2026-06-06 06:18 AM',
  'sunset': '2026-06-06 09:05 PM',
  'daylight_duration': '14h 47m',
  'next_event': 'first_light',
  'time_remaining': '9h 27m'
}

✅ All validations passed
✅ Load successful
✅ Pipeline complete
```

---

# Step 2: Run Dash Application

```bash
python app.py
```

Open in browser:
```
http://127.0.0.1:8050/
```

---
## Dependencies

- Dash
- Pandas
- Plotly
- SQLAlchemy
- psycopg2
- timezonefinder
- pytz

Install:
```bash
pip install dash pandas plotly sqlalchemy psycopg2-binary timezonefinder pytz
```

---

## Screenshots / Demo

<img width="1918" height="478" alt="image" src="https://github.com/user-attachments/assets/45aaa110-fc78-48b1-82b7-da232c089896" />

<img width="1918" height="1027" alt="image" src="https://github.com/user-attachments/assets/d4449d9d-4b66-4940-88c2-2ebd6cb9f525" />

---

## Business Insights

This dashboard provides insights into solar conditions across cities:

### Outdoor Planning
- Sunrise and sunset times
- Daylight duration
- Best time for outdoor activity

### Time Sensitivity
- Time remaining until next solar event
- Helps users plan around daylight

---

## ETL Pipeline Summary

- Extract: Sunrise-Sunset API
- Transform: timezone conversion + feature engineering
- Load: PostgreSQL
- Visualize: Dash dashboard
