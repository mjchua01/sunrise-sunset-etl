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

## Project Structure

Summer 2026/
│
├── extract.py         # API extraction layer
├── transform.py       # Data cleaning + feature engineering
├── load.py            # PostgreSQL loading via SQLAlchemy
├── validation.py      # Data quality checks
├── main.py            # ETL pipeline runner
├── requirements.txt   # Dependencies
├── .gitignore         # Files excluded from version control
└── README.md

## ETL Pipeline

### Extract
- Retrieves latitude/longitude using OpenStreetMap Geocoding API  
- Retrieves sunrise/sunset data from Sunrise-Sunset API  
- Includes retry logic and logging  

### Transform
- Converts UTC timestamps to local time  
- Calculates daylight duration  
- Determines next light event  
- Selects correct cycle (today or next day)  

### Validation
- Null value checks  
- Schema validation  
- Format validation  
- Logical consistency checks  

### Load
- Loads transformed data into PostgreSQL using SQLAlchemy  
- Stores results in `sun_cycle` table  

## 🛠️ Technologies Used

Python 3.x, Requests, Pandas, SQLAlchemy, PostgreSQL, psycopg2, timezonefinder  

## ⚙️ Setup Instructions

### 1. Navigate to project folder
cd path\to\your\project\folder

### 2. Install dependencies
pip install -r requirements.txt

### 3. Create PostgreSQL database
CREATE DATABASE sunrise_db;

### 4. Run project
python main.py

## Example Output

Enter a city: Clarksville, IN

Extract successful  
Transform successful  
Validation successful  
Load successful  

FINAL DATA:
{
  "city": "Clarksville, IN",
  "sunrise": "06:21 AM",
  "sunset": "08:58 PM",
  "daylight_duration": "14h 36m",
  "next_event": "sunset",
  "time_remaining": "2h 19m"
}

## Data Quality Checks

- Null value checks  
- Schema validation  
- Format validation  
- Logical checks  

## Notes

- Automatically selects correct daylight cycle  
- Timezone derived from coordinates  
- API retry logic included  
