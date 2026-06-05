# Infrastructure Specification

## Purpose
This specification defines the data persistence layer and the user interface layout for the Vivienda MVP.

## Requirements

### Requirement: Persistence Layer (SQLite)
The system MUST use SQLite for local data storage.

#### Scenario: Rental Data Schema
- GIVEN a newly scraped listing
- WHEN stored in the database
- THEN it MUST be persisted in a `listings` table with the following schema:
    - `id` (INT, PK)
    - `city` (TEXT)
    - `price` (REAL)
    - `rooms` (INT)
    - `surface` (REAL)
    - `date` (DATE)
    - `source` (TEXT)

#### Scenario: Salary Data Schema
- GIVEN an INDEC salary import
- WHEN stored in the database
- THEN it MUST be persisted in a `salaries` table:
    - `city` (TEXT, PK)
    - `tier_min` (REAL)
    - `tier_median` (REAL)
    - `tier_prof` (REAL)
    - `updated_at` (DATE)

### Requirement: UI Layout (Streamlit)
The system SHALL implement a clean, interactive dashboard layout.

#### Scenario: Dashboard Structure
- GIVEN the application start
- WHEN the page loads
- THEN it MUST display:
    - **Sidebar**: Salary Tier Selector (Dropdown: Min, Median, Professional).
    - **Main Area**:
        - Row 1: Header and Summary Stats.
        - Row 2: The DII Choropleth Map.
        - Row 3: Bubble Chart and Leaderboard (Side-by-side).

## Acceptance Criteria
- Database schema correctly stores all required fields without data loss.
- Streamlit sidebar interaction triggers a full re-render of the analytical components.
- Application layout remains responsive on standard desktop resolutions.

## Edge Case Handling
- **DB Connection Failure**: If SQLite is unreachable, the system MUST display a friendly error message: "Error connecting to data store. Please check database path."
- **Schema Version Mismatch**: If the DB schema is outdated, the system SHOULD attempt to migrate the schema or notify the user to clear the `data/` directory.
