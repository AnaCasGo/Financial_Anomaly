from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "01_raw"
PROCESSED_DATA_DIR = DATA_DIR / "02_processed"

CUSTOMERS_PATH = RAW_DATA_DIR / "customers.csv"
MERCHANTS_PATH = RAW_DATA_DIR / "merchants.csv"
BEHAVIOR_PROFILE_PATH = PROCESSED_DATA_DIR / "customer_behavior_profile.csv"


# ============================================================
# REPRODUCIBILITY
# ============================================================

RANDOM_SEED = 42


# ============================================================
# POPULATION
# ============================================================

N_CUSTOMERS = 500
N_MERCHANTS = 250


# ============================================================
# HISTORICAL / PRODUCTION PERIODS
# ============================================================

HISTORICAL_START = "2025-01-01"
HISTORICAL_END = "2025-12-31"

PRODUCTION_START = "2026-01-01"
PRODUCTION_END = "2026-01-31"


# ============================================================
# DEMOGRAPHICS
# ============================================================

MIN_CUSTOMER_AGE = 18
MAX_CUSTOMER_AGE = 90


# Approximate Spanish / foreign population structure.
# These are used as modelling assumptions, not as exact
# representation of the Spanish banking population.

NATIONALITY_SPANISH_PROBABILITY = 0.859
NATIONALITY_FOREIGN_PROBABILITY = 0.141


# ============================================================
# HISTORICAL CONTAMINATION
# ============================================================

# Historical data is mostly normal, but not perfectly clean.

HISTORICAL_ANOMALY_RATE = 0.015

# Production anomaly rate can be somewhat higher so that
# the detection system has enough cases to evaluate.

PRODUCTION_ANOMALY_RATE = 0.02