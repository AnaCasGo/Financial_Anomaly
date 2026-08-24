import numpy as np
import pandas as pd

from config import RANDOM_SEED


# ============================================================
# CONFIGURATION
# ============================================================

# Expected transactions per month by employment status.
#
# These are modelling assumptions used to create behavioural
# heterogeneity. They are not estimates of actual Spanish
# banking behaviour.

BASE_TRANSACTIONS_PER_MONTH = {
    "Employed": 35,
    "Self-employed": 45,
    "Unemployed": 18,
    "Student": 25,
    "Retired": 22,
    "Other": 20,
}


# Typical transaction amount by employment status.

BASE_TRANSACTION_AMOUNT = {
    "Employed": 45,
    "Self-employed": 65,
    "Unemployed": 30,
    "Student": 25,
    "Retired": 40,
    "Other": 35,
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def generate_transaction_frequency(rng: np.random.Generator,employment_status: str,) -> float:
    """
    Generate the expected number of transactions per month.

    A log-normal distribution is used to introduce individual
    heterogeneity while keeping the value positive.
    """

    base = BASE_TRANSACTIONS_PER_MONTH[employment_status]

    frequency = rng.lognormal(
        mean=np.log(base),
        sigma=0.35,
    )

    return float(frequency)


def generate_typical_amount(rng: np.random.Generator,employment_status: str,) -> float:
    """
    Generate the customer's typical transaction amount.
    """

    base = BASE_TRANSACTION_AMOUNT[employment_status]

    amount = rng.lognormal(
        mean=np.log(base),
        sigma=0.40,
    )

    return float(amount)


def generate_amount_variability(rng: np.random.Generator,) -> float:
    """
    Generate transaction amount variability.

    Higher values mean that the customer's transaction amounts
    are more dispersed around their typical spending level.
    """

    return float(
        rng.uniform(
            0.25,
            0.75,
        )
    )


def generate_online_probability(rng: np.random.Generator,age: int,occupation: str,) -> float:
    """
    Generate probability of making an online transaction.

    Age has a probabilistic influence, but substantial
    individual-level variability is retained.
    """

    if age < 25:
        base = 0.65

    elif age < 40:
        base = 0.55

    elif age < 60:
        base = 0.40

    elif age < 75:
        base = 0.25

    else:
        base = 0.15

    # Some occupations are naturally more compatible with digital/online activity.

    digital_occupations = {
        "Science and engineering professional",
        "Business and management professional",
        "Administrative worker",
        "Accounting and financial support worker",
    }

    if occupation in digital_occupations:
        base += 0.10

    # Individual variation
    probability = base + rng.normal(
        loc=0,
        scale=0.10,
    )

    return float(
        np.clip(
            probability,
            0.02,
            0.95,
        )
    )


def generate_international_probability(rng: np.random.Generator,nationality: str,) -> float:
    """
    Generate probability of an international transaction.

    Nationality may influence legitimate international activity,
    but it does not influence fraud probability.
    """

    if nationality == "Spain":
        base = 0.05

    else:
        base = 0.12

    probability = base + rng.normal(
        loc=0,
        scale=0.04,
    )

    return float(
        np.clip(
            probability,
            0.005,
            0.50,
        )
    )


def generate_night_probability(rng: np.random.Generator,age: int,employment_status: str,) -> float:
    """
    Probability of transactions occurring during night hours.
    """

    base = 0.05

    if age < 30:
        base += 0.08

    elif age < 45:
        base += 0.04

    if employment_status == "Student":
        base += 0.05

    probability = base + rng.normal(
        loc=0,
        scale=0.025,
    )

    return float(
        np.clip(
            probability,
            0.005,
            0.40,
        )
    )


def generate_weekend_probability(rng: np.random.Generator,employment_status: str,) -> float:
    """
    Probability that a transaction occurs during the weekend.
    """

    base = {
        "Employed": 0.28,
        "Self-employed": 0.25,
        "Unemployed": 0.30,
        "Student": 0.38,
        "Retired": 0.22,
        "Other": 0.28,
    }[employment_status]

    probability = base + rng.normal(
        loc=0,
        scale=0.05,
    )

    return float(
        np.clip(
            probability,
            0.05,
            0.60,
        )
    )


def generate_number_of_devices(rng: np.random.Generator,age: int,online_probability: float,) -> int:
    """
    Generate the number of devices normally used by a customer.
    """

    base_lambda = 1.0

    if age < 40:
        base_lambda += 0.5

    if online_probability > 0.60:
        base_lambda += 0.4

    number_of_devices = 1 + rng.poisson(
        lam=base_lambda
    )

    return int(
        np.clip(
            number_of_devices,
            1,
            6,
        )
    )


def generate_geographic_mobility(rng: np.random.Generator,employment_status: str,occupation: str,) -> float:
    """
    Generate a latent geographic mobility score.

    Higher values indicate that the customer is more likely to
    transact outside their usual city.
    """

    base = 0.30

    if employment_status == "Self-employed":
        base += 0.15

    if occupation in {
        "Driver",
        "Sales representative"
    }:
        base += 0.20

    mobility = base + rng.normal(
        loc=0,
        scale=0.12,
    )

    return float(
        np.clip(
            mobility,
            0.01,
            0.95,
        )
    )


# ============================================================
# MAIN GENERATOR
# ============================================================

def generate_behavior_profiles(customers: pd.DataFrame,seed: int = RANDOM_SEED,) -> pd.DataFrame:
    """
    Generate latent behavioural parameters for each customer.

    These parameters are internal to the synthetic data
    generation process and are not intended to represent
    observed customer behaviour.
    """

    rng = np.random.default_rng(seed)

    profiles = []

    for _, customer in customers.iterrows():

        age = (
            pd.Timestamp("2025-01-01")
            - pd.Timestamp(customer["date_of_birth"])
        ).days // 365

        employment_status = customer[
            "employment_status"
        ]

        occupation = customer[
            "occupation"
        ]

        nationality = customer[
            "nationality"
        ]

        expected_transactions = (
            generate_transaction_frequency(
                rng,
                employment_status,
            )
        )

        typical_amount = (
            generate_typical_amount(
                rng,
                employment_status,
            )
        )

        amount_variability = (
            generate_amount_variability(
                rng,
            )
        )

        online_probability = (
            generate_online_probability(
                rng,
                age,
                occupation,
            )
        )

        international_probability = (
            generate_international_probability(
                rng,
                nationality,
            )
        )

        night_probability = (
            generate_night_probability(
                rng,
                age,
                employment_status,
            )
        )

        weekend_probability = (
            generate_weekend_probability(
                rng,
                employment_status,
            )
        )

        number_of_devices = (
            generate_number_of_devices(
                rng,
                age,
                online_probability,
            )
        )

        geographic_mobility = (
            generate_geographic_mobility(
                rng,
                employment_status,
                occupation,
            )
        )

        profiles.append(
            {
                "customer_id": customer[
                    "customer_id"
                ],
                "latent_expected_transactions_month":
                    expected_transactions,
                "latent_typical_transaction_amount":
                    typical_amount,
                "latent_amount_variability":
                    amount_variability,
                "latent_online_probability":
                    online_probability,
                "latent_international_probability":
                    international_probability,
                "latent_night_probability":
                    night_probability,
                "latent_weekend_probability":
                    weekend_probability,
                "latent_number_of_devices":
                    number_of_devices,
                "latent_geographic_mobility":
                    geographic_mobility,
            }
        )

    return pd.DataFrame(profiles)


# ============================================================
# SCRIPT EXECUTION
# ============================================================

if __name__ == "__main__":

    from generate_customers import generate_customers

    customers = generate_customers()

    profiles = generate_behavior_profiles(
        customers
    )

    print("\nLatent behavioural profiles:")
    print(
        profiles.head()
    )

    print("\nShape:")
    print(
        profiles.shape
    )

    print("\nDescriptive statistics:")
    print(
        profiles.describe()
    )