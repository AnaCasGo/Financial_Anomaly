import numpy as np
import pandas as pd

from config import (
    N_MERCHANTS,
    RANDOM_SEED,
)


# ============================================================
# MERCHANT CATEGORIES
# ============================================================

MERCHANT_CATEGORIES = [
    "Grocery",
    "Restaurants",
    "Transport",
    "Travel",
    "Entertainment",
    "Electronics",
    "Clothing",
    "Healthcare",
    "Utilities",
    "Education",
    "Hotels",
    "Jewellery",
    "Luxury Goods",
    "Online Services",
]


# Categories should not have equal representation.
# Everyday categories are more common than luxury categories.

MERCHANT_CATEGORY_WEIGHTS = [
    0.16,  # Grocery
    0.14,  # Restaurants
    0.10,  # Transport
    0.06,  # Travel
    0.08,  # Entertainment
    0.07,  # Electronics
    0.09,  # Clothing
    0.06,  # Healthcare
    0.06,  # Utilities
    0.04,  # Education
    0.05,  # Hotels
    0.02,  # Jewellery
    0.02,  # Luxury Goods
    0.05,  # Online Services
]


# ============================================================
# GEOGRAPHY
# ============================================================

SPANISH_CITIES = [
    "Madrid",
    "Barcelona",
    "Valencia",
    "Seville",
    "Zaragoza",
    "Málaga",
    "Murcia",
    "Palma",
    "Las Palmas de Gran Canaria",
    "Bilbao",
    "Alicante",
    "Córdoba",
    "Valladolid",
    "Vigo",
    "Gijón",
]


SPANISH_CITY_WEIGHTS = [
    0.24,
    0.17,
    0.09,
    0.07,
    0.06,
    0.06,
    0.05,
    0.04,
    0.04,
    0.04,
    0.04,
    0.03,
    0.03,
    0.02,
    0.02,
]


INTERNATIONAL_LOCATIONS = [
    ("Paris", "France"),
    ("Rome", "Italy"),
    ("Lisbon", "Portugal"),
    ("London", "United Kingdom"),
    ("Berlin", "Germany"),
    ("Amsterdam", "Netherlands"),
    ("New York", "United States"),
    ("Miami", "United States"),
    ("Dubai", "United Arab Emirates"),
    ("Mexico City", "Mexico"),
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def generate_merchant_categories(rng: np.random.Generator,n: int,) -> np.ndarray:
    """
    Generate merchant categories using weighted probabilities.
    """

    return rng.choice(
        MERCHANT_CATEGORIES,
        size=n,
        p=np.array(MERCHANT_CATEGORY_WEIGHTS)
        / np.sum(MERCHANT_CATEGORY_WEIGHTS),
    )


def generate_merchant_location(rng: np.random.Generator,category: str,) -> tuple[str, str]:
    """
    Generate a merchant location.

    Most merchants are located in Spain, while some categories
    have a higher probability of being international.
    """

    international_probabilities = {
        "Grocery": 0.02,
        "Restaurants": 0.03,
        "Transport": 0.05,
        "Travel": 0.30,
        "Entertainment": 0.08,
        "Electronics": 0.10,
        "Clothing": 0.10,
        "Healthcare": 0.02,
        "Utilities": 0.01,
        "Education": 0.02,
        "Hotels": 0.25,
        "Jewellery": 0.15,
        "Luxury Goods": 0.25,
        "Online Services": 0.20,
    }

    international_probability = international_probabilities.get(
        category,
        0.05,
    )

    if rng.random() < international_probability:

        city, country = INTERNATIONAL_LOCATIONS[
            rng.integers(0, len(INTERNATIONAL_LOCATIONS))
        ]

        return city, country

    city = rng.choice(
        SPANISH_CITIES,
        p=np.array(SPANISH_CITY_WEIGHTS)
        / np.sum(SPANISH_CITY_WEIGHTS),
    )

    return city, "Spain"


# ============================================================
# MAIN GENERATOR
# ============================================================

def generate_merchants(n_merchants: int = N_MERCHANTS,seed: int = RANDOM_SEED,) -> pd.DataFrame:
    """
    Generate the synthetic merchant population.
    """

    rng = np.random.default_rng(seed)

    merchant_ids = [
        f"M{i:04d}"
        for i in range(1, n_merchants + 1)
    ]

    categories = generate_merchant_categories(
        rng,
        n_merchants,
    )

    locations = [
        generate_merchant_location(
            rng,
            category,
        )
        for category in categories
    ]

    cities = [
        location[0]
        for location in locations
    ]

    countries = [
        location[1]
        for location in locations
    ]

    merchants = pd.DataFrame(
        {
            "merchant_id": merchant_ids,
            "merchant_category": categories,
            "country": countries,
            "city": cities,
        }
    )

    return merchants


# ============================================================
# SCRIPT EXECUTION
# ============================================================

if __name__ == "__main__":

    merchants = generate_merchants()

    print("\nMerchant dataset:")
    print(merchants.head())

    print("\nDataset shape:")
    print(merchants.shape)

    print("\nMerchant categories:")
    print(
        merchants["merchant_category"]
        .value_counts()
    )

    print("\nMerchant countries:")
    print(
        merchants["country"]
        .value_counts()
    )