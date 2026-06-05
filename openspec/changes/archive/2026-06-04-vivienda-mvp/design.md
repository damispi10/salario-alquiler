# Design: Vivienda MVP - Salary vs Rent Optimizer

## Technical Approach

The system will be implemented as a modular Python application following a decoupled pipeline architecture: **Collection $\rightarrow$ Storage $\rightarrow$ Analysis $\rightarrow$ Presentation**.

The application separates the volatile "scraping" phase from the "analytical" phase using a local SQLite database as the single source of truth. This ensures that the Streamlit UI remains responsive and the analytical engine has a stable dataset to operate on regardless of scraper status.

## Architecture Decisions

### Decision: Storage Engine
**Choice**: SQLite
**Alternatives considered**: CSV/JSON, PostgreSQL
**Rationale**: Low overhead, zero configuration for MVP, and sufficient performance for the expected volume of regional rental listings.

### Decision: Scraping Strategy
**Choice**: Playwright (Headless) with custom rotation
**Alternatives considered**: BeautifulSoup (static), Scrapy
**Rationale**: Zonaprop and Mercado Libre heavily rely on JavaScript rendering and bot detection. Playwright provides the necessary browser emulation and stealth capabilities.

### Decision: UI Framework
**Choice**: Streamlit
**Alternatives considered**: Flask/React, Plotly Dash
**Rationale**: Extremely high development velocity for data-focused dashboards. Built-in state management handles the "Salary Tier" selection seamlessly.

## Data Flow

The pipeline operates linearly, with a feedback loop for the UI.

```
[Web Portals] --(Playwright)--> [Collector] --(SQLAlchemy)--> [SQLite DB]
                                                                 │
                                                                 ▼
[Streamlit UI] <--(Plotly)-- [Visualizer] <--(Pandas)-- [AffordabilityEngine]
      │                                                           ▲
      └────(Salary Tier Selection)────────────────────────────────┘
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `src/scraper/rental_scraper.py` | Create | Playwright logic for Zonaprop/ML and data cleaning |
| `src/scraper/salary_import.py` | Create | Logic to normalize and import INDEC CSV/PDF data |
| `src/engine/affordability.py` | Create | `AffordabilityEngine` class implementing DII formula |
| `src/ui/visualizer.py` | Create | Plotly wrappers for Maps, Bubble Charts and Leaderboards |
| `src/ui/app.py` | Create | Streamlit main entry point and state management |
| `src/db/schema.py` | Create | SQLAlchemy models for `listings` and `salaries` |
| `data/vivienda.db` | Create | SQLite database file |
| `config.yaml` | Create | Scraper settings (delays, User-Agents, exchange rates) |

## Interfaces / Contracts

### Database Schema (SQLAlchemy)

```python
class RentalListing(Base):
    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    price = Column(Float)
    rooms = Column(Integer)
    surface = Column(Float)
    date = Column(Date)
    source = Column(String) # 'zonaprop' | 'mercadolibre'

class RegionalSalary(Base):
    __tablename__ = 'salaries'
    city = Column(String, primary_key=True)
    tier_min = Column(Float)
    tier_median = Column(Float)
    tier_prof = Column(Float)
    updated_at = Column(Date)
```

### Core Class Definitions

#### `RentalScraper`
- `scrape_city(city_name: str)`: Launches Playwright, iterates pages, extracts raw listing data.
- `clean_data(raw_html: str)`: Cleans currency symbols, handles "consultar" prices, and normalizes to float.
- `save_to_db(data: List[Dict])`: Batch inserts cleaned data into the `listings` table.

#### `AffordabilityEngine`
- `get_city_metrics(city: str, tier: str)`: Returns average rent and corresponding salary for the tier.
- `calculate_dii(salary: float, rent: float) -> float`: Implements $DII = \\frac{Salary - (Rent * 1.15)}{Rent}$.
- `get_leaderboard(tier: str)`: Returns a sorted list of cities by DII.

#### `Visualizer`
- `plot_choropleth(df_dii)`: Returns a Plotly map object.
- `plot_bubble_chart(df_metrics)`: Returns a Plotly bubble chart showing Rent vs Salary.
- `render_leaderboard(df_ranked)`: Returns a Streamlit dataframe/table.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | DII Formula | Pytest with fixed salary/rent inputs (verify 2.18 result) |
| Integration | Scraper $\rightarrow$ DB | Run scraper on 1 city $\rightarrow$ verify record count in SQLite |
| E2E | UI $\rightarrow$ Engine | Change salary tier in Streamlit $\rightarrow$ verify map colors update |

## Migration / Rollout

No migration required for MVP. Initial setup includes a `seed_salaries.py` script to populate the initial INDEC data.

## Open Questions

- [ ] Which specific GeoJSON file will be used for the Southern BA province boundaries?
- [ ] Should we implement a "Refresh Data" button in the UI or rely on a separate cron job for scraping?
