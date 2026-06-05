# Data Acquisition Specification

## Purpose
This specification defines the automated extraction of rental data from real estate portals and the integration of official salary data to feed the analytical engine.

## Requirements

### Requirement: Rental Scraping Engine
The system MUST extract rental listing data from Zonaprop and Mercado Libre for cities in the south of Buenos Aires province.

#### Scenario: Successful Extraction
- GIVEN a target city list and active portal URLs
- WHEN the scraper runs
- THEN the system MUST capture: Price, City, Rooms, Surface, and Date
- AND store them in the SQLite database with a timestamp

#### Scenario: Anti-Scraping Mitigation
- GIVEN a portal implementing rate limits or bot detection
- WHEN the scraper requests pages
- THEN it MUST use headless mode and rotate User-Agent headers
- AND implement a random delay (1-5s) between requests to avoid blocks

### Requirement: Salary Data Integration
The system SHALL integrate regional salary data from INDEC.

#### Scenario: INDEC Data Import
- GIVEN an INDEC salary dataset (CSV/PDF)
- WHEN the import process is triggered
- THEN the system MUST normalize salary values to a consistent currency/index
- AND map salaries to the corresponding city/region identifiers used in rental data

#### Scenario: Handling Missing Salary Data
- GIVEN a city with no specific INDEC salary record
- WHEN the system calculates the index
- THEN it SHOULD fall back to the regional average salary for Southern BA

## Acceptance Criteria
- Successfully extract rental data from both Zonaprop and Mercado Libre.
- Data contains all 5 required fields (Price, City, Rooms, Surface, Date).
- Salary data is correctly mapped to city names.
- Scraper operates without being blocked for a full regional sweep.

## Edge Case Handling
- **Zero Listings**: If a city has 0 listings, mark the city as "Insufficient Data" and exclude from DII calculation.
- **Extreme Outliers**: Listings with prices +/- 3 standard deviations from the city mean MUST be flagged or excluded to prevent DII skew.
- **Currency Mismatch**: If listings are in USD and Salaries in ARS, the system MUST use a configured exchange rate to normalize.
