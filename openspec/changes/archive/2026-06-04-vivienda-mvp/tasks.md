# Tasks: Vivienda MVP - Salary vs Rent Optimizer

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 600 - 900 |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 (Infra/DB) $\rightarrow$ PR 2 (Scraping/Import) $\rightarrow$ PR 3 (Engine/UI) |
| Delivery strategy | ask-on-risk |
| Chain strategy | feature-branch-chain |

Decision needed before apply: Yes
Chained PRs recommended: Yes
Chain strategy: feature-branch-chain
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Foundational Infrastructure | PR 1 | Base branch; Schema, Config, and DB layer. |
| 2 | Data Acquisition Pipeline | PR 2 | Depends on PR 1; Playwright scrapers and INDEC import. |
| 3 | Analysis and Dashboard | PR 3 | Depends on PR 2; DII logic, Plotly visuals, and Streamlit app. |

## Phase 1: Infrastructure & Data Model

- [ ] 1.1 Create `config.yaml` with scraper settings, User-Agents, and exchange rates.
- [ ] 1.2 Implement `src/db/schema.py` using SQLAlchemy definitions for `RentalListing` and `RegionalSalary` tables.
- [ ] 1.3 Implement database connection utility in `src/db/connection.py` with error handling for unreachable store.
- [ ] 1.4 Create a seed script `src/db/seed_salaries.py` to populate initial INDEC data into `salaries` table.
- [ ] 1.5 Verify: Run seed script and check `data/vivienda.db` for expected rows in `salaries`.

## Phase 2: Data Acquisition

- [ ] 2.1 Implement `src/scraper/rental_scraper.py` with Playwright headless logic for Zonaprop and Mercado Libre.
- [ ] 2.2 Implement rotation of User-Agents and random delays (1-5s) in `RentalScraper` to mitigate bot detection.
- [ ] 2.3 Implement `clean_data()` in `RentalScraper` to normalize prices, remove symbols, and handle "consultar" values.
- [ ] 2.4 Implement `src/scraper/salary_import.py` to process INDEC CSV/PDF data and map to city identifiers.
- [ ] 2.5 Implement fallback logic in `salary_import.py` to use regional averages for cities with missing data.
- [ ] 2.6 Verify: Run scraper for one city and verify `listings` table is populated with 5 required fields.

## Phase 3: Analytical Engine

- [ ] 3.1 Implement `AffordabilityEngine` in `src/engine/affordability.py` implementing the formula $DII = \frac{Salary - (Rent * 1.15)}{Rent}$.
- [ ] 3.2 Implement `get_city_metrics()` to fetch average rent and mapped salary based on selected tier (Min, Median, Prof).
- [ ] 3.3 Implement `get_leaderboard()` to return cities sorted by DII in descending order.
- [ ] 3.4 Implement handling for negative DII and division-by-zero (Rent=0) resulting in `NaN`.
- [ ] 3.5 Verify: Write Pytest for DII formula verifying the 2.18 result for the standard scenario.

## Phase 4: Visualization & UI

- [ ] 4.1 Implement `src/ui/visualizer.py` with `plot_choropleth` using Plotly and a red-yellow-green color scale.
- [ ] 4.2 Implement `plot_bubble_chart` in `visualizer.py` mapping Average Rent (X), Salary (Y), and Listing Count (Size).
- [ ] 4.3 Implement `render_leaderboard` using Streamlit dataframes to show the Top 5 affordable cities.
- [ ] 4.4 Implement `src/ui/app.py` as the Streamlit entry point with Sidebar tier selector and the layout specified in infrastructure spec.
- [ ] 4.5 Verify: Launch Streamlit app and verify that changing the salary tier updates the map and leaderboard instantly.

## Phase 5: Integration & Polishing

- [ ] 5.1 Implement data outlier filtering (±3 std dev) in the `AffordabilityEngine` before calculating city averages.
- [ ] 5.2 Implement currency normalization in `RentalScraper` using `config.yaml` exchange rates if listings are in USD.
- [ ] 5.3 Perform E2E test: Run full pipeline (Scrape $\rightarrow$ Import $\rightarrow$ Analyze $\rightarrow$ Render) and verify consistency.
- [ ] 5.4 Final Polish: Add "Insufficient Data" labels for cities with zero listings on the map.
- [ ] 5.5 Verify: Confirm application loads within a local Docker container as per success criteria.
