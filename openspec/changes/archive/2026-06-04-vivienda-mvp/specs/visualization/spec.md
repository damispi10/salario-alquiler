# Visualization Specification

## Purpose
This specification defines the visual representation of the Disposable Income Index and rental trends to enable intuitive comparison of city affordability.

## Requirements

### Requirement: DII Choropleth Map
The system MUST provide a geospatial visualization of the Southern BA province.

#### Scenario: Map Color Coding
- GIVEN a set of calculated DII values per city
- WHEN the map is rendered
- THEN cities MUST be color-coded based on DII:
    - Green: High DII (Very Affordable)
    - Yellow: Moderate DII
    - Red: Low/Negative DII (Expensive/Unviable)

### Requirement: Rent vs Salary Bubble Chart
The system SHALL provide a statistical correlation chart.

#### Scenario: Bubble Mapping
- GIVEN rental and salary data
- WHEN the chart renders
- THEN it MUST plot:
    - X-axis: Average Rent
    - Y-axis: Regional Salary
    - Bubble Size: Number of available listings (representing data confidence)

### Requirement: Affordability Leaderboard
The system MUST provide a ranked tabular view of the best cities.

#### Scenario: Ranking Logic
- GIVEN all cities with valid DII
- WHEN the leaderboard is requested
- THEN the system MUST sort cities by DII in descending order and display the top 5.

## Acceptance Criteria
- Map correctly distinguishes between high and low DII regions.
- Bubble chart accurately represents the relationship between rent, salary, and sample size.
- Leaderboard updates instantly when the salary tier is changed.

## Edge Case Handling
- **Zero Data Cities**: Cities with no data MUST be colored grey on the map and excluded from the leaderboard.
- **Scale Overflow**: If a city has an extreme DII (outlier), the color scale MUST be clamped to a reasonable range (e.g., 0 to 5) to maintain visual contrast for other cities.
