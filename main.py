#!/usr/bin/env python3
"""
Vivienda MVP - Main Entry Point

Orchestrates the data pipeline:
1. Scrapes rental data and loads salary baselines
2. Stores results in the local SQLite database
3. Launches the Streamlit dashboard

Usage:
    python main.py --scrape      # Refresh data before launching UI
    python main.py --ui          # Launch dashboard only
    python main.py               # Full pipeline (scrape + launch UI)
"""

import argparse
import asyncio
import subprocess
import sys
from pathlib import Path

# Ensure src/ modules are importable
sys.path.insert(0, str(Path(__file__).parent / "src"))

from scraper.rental_scraper import RentalScraper
from scraper.salary_loader import SalaryLoader
from db.manager import DBManager

CITIES = ["La Plata", "Bahía Blanca", "Mar del Plata", "Tandil", "Necochea"]


def run_scraper():
    """Gather fresh rental listings and salary data."""
    db = DBManager()

    print("🕵️  Scraping rental listings...")
    scraper = RentalScraper(db)
    asyncio.run(scraper.run(CITIES))

    print("💰 Loading salary baselines...")
    loader = SalaryLoader(db)
    loader.load_indec_data()

    print("✅ Data pipeline complete.\n")


def launch_ui():
    """Start the Streamlit dashboard."""
    print("🚀 Launching Streamlit dashboard...")
    ui_path = Path(__file__).parent / "src" / "ui" / "app.py"
    subprocess.run(["streamlit", "run", str(ui_path)], check=True)


def main():
    parser = argparse.ArgumentParser(description="Vivienda DII Index Pipeline")
    parser.add_argument(
        "--scrape",
        action="store_true",
        help="Run scrapers to refresh rental and salary data",
    )
    parser.add_argument(
        "--ui",
        action="store_true",
        help="Launch the Streamlit dashboard only (skip scraping)",
    )
    args = parser.parse_args()

    if args.scrape and args.ui:
        run_scraper()
        launch_ui()
    elif args.scrape:
        run_scraper()
    elif args.ui:
        launch_ui()
    else:
        run_scraper()
        launch_ui()


if __name__ == "__main__":
    main()
