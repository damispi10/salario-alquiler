# Proposal: Vivienda MVP - Salary vs Rent Optimizer

## Intent

The goal is to build a decision-support tool that identifies the most economically advantageous cities in the south of Buenos Aires province. By calculating the ratio between regional salaries and average rents, the application aims to surface locations that maximize disposable income, helping users make data-driven decisions about where to live and work.

## Scope

### In Scope
- **Data Pipeline**:
    - Web scrapers for Zonaprop and Mercado Libre using Playwright/BeautifulSoup.
    - Integration of INDEC regional salary datasets.
    - Inflation mitigation strategy (USD indexing or high-frequency refreshes).
- **Analytical Core**:
    - Implementation of the Disposable Income Index (DII).
    - Segmentation by housing type (e.g., standard 2-room apartment).
    - Analysis across salary tiers (Minimum, Median, Professional).
- **Visualization Suite**:
    - Interactive Choropleth Map of Southern BA province.
    - Rent vs Salary correlation bubble chart.
    - Top 5 'most affordable' cities leaderboard.
- **Interface**:
    - Streamlit-based interactive dashboard.

### Out of Scope
- Real-time price alerts or notifications.
- Detailed neighborhood-level analysis (focus is city-level).
- Support for other provinces.
- Multi-user authentication or personalized profiles.

## Capabilities

### New Capabilities
- `data-scraping`: Automated extraction of rental prices from real estate portals.
- `salary-integration`: Processing and normalization of INDEC regional salary data.
- `dii-calculator`: Engine to compute the Disposable Income Index based on rent and salary.
- `economic-viz`: Generation of geospatial and statistical charts for cost-of-living analysis.
- `vivienda-dashboard`: Streamlit interface for interacting with the analytical core.

### Modified Capabilities
- None

## Approach

The project will follow a modular data-driven pipeline:
1. **Extraction**: Scripts to poll real estate sites and INDEC PDFs/CSVs.
2. **Storage**: A lightweight SQLite database to store historical and current snapshots.
3. **Transformation**: Pandas-based cleaning and normalization (converting all values to a stable currency/index).
4. **Presentation**: A Streamlit app serving as the frontend for Plotly visualizations.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `src/scraping` | New | Playwright/BeautifulSoup logic for portals |
| `src/analytics` | New | DII formula and data normalization logic |
| `src/ui` | New | Streamlit dashboard and Plotly components |
| `data/` | New | SQLite database and raw data dumps |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Anti-scraping blocks | High | Use rotating user-agents, headless mode, and request throttling |
| Data sparsity (small towns) | Medium | Implement minimum sample size thresholds; mark low-confidence cities |
| High inflation volatility | High | Index data to USD or implement a weekly refresh cycle |

## Rollback Plan

Since this is an MVP, the rollback plan involves:
- Reverting the codebase to the last stable commit via Git.
- Purging the SQLite data store if schema corruption occurs.

## Dependencies

- **Python Libraries**: Pandas, Plotly, Streamlit, Playwright, SQLAlchemy.
- **External Data**: Zonaprop, Mercado Libre, INDEC.

## Success Criteria

- [ ] Successfully scrape rental data for at least 10 major cities in Southern BA.
- [ ] Correctly map INDEC salary data to the corresponding geographical areas.
- [ ] Render a Choropleth map showing the DII across the region.
- [ ] Provide a ranked list of Top 5 cities based on the DII.
- [ ] Dashboard loads and is interactive within a local Docker container.
