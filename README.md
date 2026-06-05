# Vivienda MVP
Index of affordability (DII) for rentals in the South BA province.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

## Running the Application
Start the visualization dashboard:
```bash
streamlit run src/ui/app.py
```

## Project Structure
- `src/db`: SQLite schema and manager for salaries and rents.
- `src/scraper`: Logic to gather rental data and salary baselines.
- `src/engine`: Core DII mathematical model.
- `src/ui`: Streamlit dashboard for visualization.
