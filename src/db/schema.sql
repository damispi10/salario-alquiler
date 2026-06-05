CREATE TABLE IF NOT EXISTS regional_salaries (
    region TEXT PRIMARY KEY,
    min_salary REAL,
    median_salary REAL,
    prof_salary REAL,
    mean_salary REAL DEFAULT 0,
    moda_salary REAL DEFAULT 0,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rental_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    price REAL,
    currency TEXT,
    source_url TEXT,
    scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
