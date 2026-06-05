# Analytical Engine Specification

## Purpose
This specification formalizes the calculation of the Disposable Income Index (DII) and the segmentation of financial tiers to allow for comparative economic analysis across cities.

## Requirements

### Requirement: DII Calculation
The system MUST compute the Disposable Income Index (DII) to quantify the financial "breathing room" for a resident.

**Formula**: $DII = \frac{Salary - (Rent + Utilities)}{Rent}$

#### Scenario: Standard Calculation
- GIVEN a monthly Salary of 1,000,000 ARS, Rent of 300,000 ARS, and Utilities at 15% of rent (45,000 ARS)
- WHEN the DII is calculated
- THEN the result MUST be $(1,000,000 - 345,000) / 300,000 = 2.18$

### Requirement: Utilities Baseline
The system SHALL assume a default baseline for utilities if not provided.

#### Scenario: Default Utility Cost
- GIVEN no specific utility data for a city
- WHEN calculating total housing cost
- THEN the system MUST apply a fixed 15% surcharge on the Rent value to account for electricity, water, and gas.

### Requirement: Salary Tier Segmentation
The system MUST support analysis across three distinct salary tiers.

#### Scenario: Tier Selection
- GIVEN the following tiers:
    - **Min**: Minimum regional wage.
    - **Median**: 50th percentile of regional income.
    - **Professional**: Top 25% of regional income.
- WHEN a user selects a tier in the dashboard
- THEN the DII must be recalculated using the corresponding salary value for each city.

## Acceptance Criteria
- DII is calculated correctly according to the formula.
- Salary tier changes immediately update the resulting DII values.
- Utilities baseline is consistently applied across all calculations.

## Edge Case Handling
- **Negative DII**: If $(Rent + Utilities) > Salary$, the DII is negative. The system MUST represent this as a financial deficit (e.g., highlighted in red on the map).
- **Extreme Rent**: If Rent is 0 or null, the DII MUST be marked as `NaN` to avoid division by zero.
- **Sparsity**: If salary data for a specific tier is missing, the system SHOULD use the Median tier as a fallback and add a "Estimated" label.
