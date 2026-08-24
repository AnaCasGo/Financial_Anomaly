from datetime import datetime

import numpy as np
import pandas as pd

from config import (
    N_CUSTOMERS,
    RANDOM_SEED,
    MIN_CUSTOMER_AGE,
    MAX_CUSTOMER_AGE,
)


# ============================================================
# DEMOGRAPHIC DISTRIBUTIONS
# ============================================================

AGE_GROUPS = [
    "18-24",
    "25-34",
    "35-44",
    "45-54",
    "55-64",
    "65-74",
    "75+",
]

# Initial adult population assumptions.
# These should be calibrated against the Spanish population
# distribution standarized from Piramide_de_poblacion_de_Espana_ES_Ano_2025_Habitantes.xlsx from INE

AGE_GROUP_PROBABILITIES = [
    0.09,
    0.14,
    0.16,
    0.19,
    0.17,
    0.13,
    0.12
]


FOREIGN_NATIONALITIES = [
    "Morocco",
    "Colombia",
    "Romania",
    "Italy",
    "Venezuela",
    "United Kingdom",
    "China",
    "Peru",
    "Ukraine",
    "Honduras",
    "Argentina",
    "Germany",
    "Ecuador",
    "France",
    "Bulgaria",
    "Paraguay",
    "Pakistan",
    "Portugal",
    "Russia",
    "Brazil",
]


# These are modelling weights rather than claims that these
# percentages exactly reproduce INE's complete nationality table.

FOREIGN_NATIONALITY_WEIGHTS = [
    0.18,
    0.11,
    0.09,
    0.06,
    0.05,
    0.04,
    0.04,
    0.04,
    0.035,
    0.03,
    0.03,
    0.025,
    0.025,
    0.025,
    0.02,
    0.02,
    0.02,
    0.02,
    0.02,
    0.02,
]


OCCUPATIONS = [
    "Education professional",
    "Retail worker",
    "Restaurant worker",
    "Healthcare professional",
    "Driver",
    "Cleaning worker",
    "Administrative worker",
    "Construction worker",
    "Sales representative",
    "Care worker",
    "Security worker",
    "Science and engineering professional",
    "Business and management professional",
    "Personal service worker",
    "Agricultural worker",
    "Accounting and financial support worker",
    "Manufacturing worker",
    "Shop owner",
]


OCCUPATION_WEIGHTS = [
    0.07,
    0.09,
    0.08,
    0.07,
    0.06,
    0.05,
    0.08,
    0.06,
    0.06,
    0.07,
    0.04,
    0.06,
    0.07,
    0.06,
    0.03,
    0.04,
    0.05,
    0.06,
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def generate_age(rng: np.random.Generator, n: int) -> np.ndarray:
    """
    Generate customer ages using predefined age groups.
    """

    groups = rng.choice(
        AGE_GROUPS,
        size=n,
        p=AGE_GROUP_PROBABILITIES,
    )

    ages = []

    age_ranges = {
        "18-24": (18, 24),
        "25-34": (25, 34),
        "35-44": (35, 44),
        "45-54": (45, 54),
        "55-64": (55, 64),
        "65-74": (65, 74),
        "75+": (75, MAX_CUSTOMER_AGE),
    }

    for group in groups:
        minimum, maximum = age_ranges[group]
        ages.append(
            rng.integers(
                minimum,
                maximum + 1,
            )
        )

    return np.array(ages)


def generate_nationality(rng: np.random.Generator,n: int,) -> np.ndarray:
    """
    Generate nationality.

    Spanish nationality is sampled first. Foreign customers
    are then assigned a nationality using weighted probabilities.
    """

    is_foreign = rng.random(n) >= 0.859

    nationalities = np.full(
        n,
        "Spain",
        dtype=object,
    )

    foreign_count = is_foreign.sum()

    if foreign_count > 0:
        nationalities[is_foreign] = rng.choice(
            FOREIGN_NATIONALITIES,
            size=foreign_count,
            p=np.array(FOREIGN_NATIONALITY_WEIGHTS)
            / np.sum(FOREIGN_NATIONALITY_WEIGHTS),
        )

    return nationalities


def generate_employment_status(rng: np.random.Generator,ages: np.ndarray,) -> np.ndarray:
    """
    Generate employment status conditional on age.
    """

    statuses = []

    for age in ages:

        if age <= 24:
            categories = [
                "Student",
                "Employed",
                "Unemployed",
                "Other",
            ]

            probabilities = [
                0.55,
                0.30,
                0.10,
                0.05,
            ]

        elif age <= 64:
            categories = [
                "Employed",
                "Self-employed",
                "Unemployed",
                "Other",
            ]

            probabilities = [
                0.68,
                0.12,
                0.12,
                0.08,
            ]

        else:
            categories = [
                "Retired",
                "Employed",
                "Self-employed",
                "Other",
            ]

            probabilities = [
                0.78,
                0.08,
                0.03,
                0.11,
            ]

        statuses.append(
            rng.choice(
                categories,
                p=probabilities,
            )
        )

    return np.array(statuses)


def generate_occupation(rng: np.random.Generator,ages: np.ndarray,employment_status: np.ndarray,) -> np.ndarray:
    """
    Generate occupation conditional on age and employment status.
    """

    occupations = []

    for age, status in zip(ages, employment_status):

        if status == "Student":
            occupation = "Student"

        elif status == "Retired":
            occupation = "Retired"

        elif status == "Unemployed":
            occupation = "Unemployed"

        elif status == "Other":
            occupation = "Other / inactive"

        else:
            occupation = rng.choice(
                OCCUPATIONS,
                p=np.array(OCCUPATION_WEIGHTS)
                / np.sum(OCCUPATION_WEIGHTS),
            )

        occupations.append(occupation)

    return np.array(occupations)


def generate_date_of_birth(rng: np.random.Generator,ages: np.ndarray,) -> pd.Series:
    """
    Convert ages into approximate dates of birth.

    The reference date is 1 January 2025.
    """

    reference_date = pd.Timestamp("2025-01-01")

    dates = []

    for age in ages:

        birthday_offset_days = rng.integers(
            0,
            365,
        )

        dob = (
            reference_date
            - pd.DateOffset(years=int(age))
            + pd.Timedelta(days=int(birthday_offset_days))
        )

        dates.append(dob)

    return pd.Series(dates)


def generate_customer_since(rng: np.random.Generator,n: int,) -> pd.Series:
    """
    Generate the date on which the customer joined the bank.

    Customers may have joined at any point between 2018 and
    the beginning of the historical period.
    """

    start = pd.Timestamp("2018-01-01")
    end = pd.Timestamp("2024-12-31")

    days = (end - start).days

    random_days = rng.integers(
        0,
        days + 1,
        size=n,
    )

    return pd.Series(
        start + pd.to_timedelta(
            random_days,
            unit="D",
        )
    )


# ============================================================
# MAIN GENERATOR
# ============================================================

def generate_customers(n_customers: int = N_CUSTOMERS,seed: int = RANDOM_SEED,) -> pd.DataFrame:
    """
    Generate the synthetic customer population.
    """

    rng = np.random.default_rng(seed)

    customer_ids = [
        f"ID_C{i:05d}"
        for i in range(1, n_customers + 1)
    ]

    ages = generate_age(
        rng,
        n_customers,
    )

    nationalities = generate_nationality(
        rng,
        n_customers,
    )

    employment_status = generate_employment_status(
        rng,
        ages,
    )

    occupation = generate_occupation(
        rng,
        ages,
        employment_status,
    )

    date_of_birth = generate_date_of_birth(
        rng,
        ages,
    )

    customer_since = generate_customer_since(
        rng,
        n_customers,
    )

    customers = pd.DataFrame(
        {
            "customer_id": customer_ids,
            "date_of_birth": date_of_birth,
            "nationality": nationalities,
            "country_of_residence": "Spain",
            "occupation": occupation,
            "employment_status": employment_status,
            "customer_since": customer_since,
        }
    )

    return customers


if __name__ == "__main__":

    customers = generate_customers()

    print("\nCustomer dataset:")
    print(customers.head())

    print("\nDataset shape:")
    print(customers.shape)

    print("\nAge distribution:")
    print(
        customers["date_of_birth"]
        .apply(
            lambda x: (
                pd.Timestamp("2025-01-01") - x
            ).days // 365
        )
        .value_counts()
        .sort_index()
    )

    print("\nNationality distribution:")
    print(
        customers["nationality"]
        .value_counts(normalize=True)
    )

    print("\nEmployment status:")
    print(
        customers["employment_status"]
        .value_counts(normalize=True)
    )