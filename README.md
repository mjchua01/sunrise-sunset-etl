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

<img width="1908" height="473" alt="image" src="https://github.com/user-attachments/assets/ab9d85d1-e487-4688-b832-eb0ebd5f1e5f" />

<img width="1915" height="1031" alt="image" src="https://github.com/user-attachments/assets/1568f03e-18d8-4f65-853c-3b7a436e6e63" />

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
