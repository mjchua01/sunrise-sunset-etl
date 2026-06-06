# Sunrise & Sunset Analytics Dashboard

## How to Run the Dash App

### 1. Activate your environment (optional but recommended)

```bash
conda activate base
```

or:

```bash
venv\Scripts\activate
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Ensure PostgreSQL is running

```sql
CREATE DATABASE sunrise_db;
```

---

### 4. Run the Dash app

```bash
python app.py
```

Open:
http://127.0.0.1:8050/

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
