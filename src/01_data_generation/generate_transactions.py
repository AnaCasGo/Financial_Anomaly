from datetime import timedelta
import numpy as np
import pandas as pd

from config import (
    RANDOM_SEED,
)
from generate_behaviour_profiles import generate_behavior_profiles
from generate_customers import generate_customers
from generate_merchants import generate_merchants


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def sample_transaction_time(
    rng: np.random.Generator,
    date: pd.Timestamp,
    night_prob: float,
) -> pd.Timestamp:
    """
    Sample a timestamp for a given date, conditioned on the night transaction probability.
    """
    is_night = rng.random() < night_prob
    if is_night:
        hour = int(rng.choice([23, 0, 1, 2, 3, 4, 5]))
    else:
        hour = int(rng.integers(6, 23))

    minute = int(rng.integers(0, 60))
    second = int(rng.integers(0, 60))

    return date.replace(hour=hour, minute=minute, second=second)


def sample_payment_method(
    rng: np.random.Generator,
    is_online: bool,
) -> str:
    """
    Select payment method based on online/in-person status.
    """
    if is_online:
        return str(
            rng.choice(
                ["Online Card", "Digital Wallet", "Bank Transfer"],
                p=[0.70, 0.20, 0.10],
            )
        )
    return str(
        rng.choice(
            ["Contactless Card", "Chip & PIN", "Cash Withdrawal"],
            p=[0.65, 0.30, 0.05],
        )
    )


# ============================================================
# MAIN GENERATOR
# ============================================================

def generate_transactions_for_range(
    start_date: str,
    end_date: str,
    anomaly_rate: float,
    customers: pd.DataFrame = None,
    merchants: pd.DataFrame = None,
    profiles: pd.DataFrame = None,
    seed: int = RANDOM_SEED,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generates transactions and ground truth metadata for a specific date range.
    """
    rng = np.random.default_rng(seed)

    if customers is None:
        customers = generate_customers(seed=seed)
    if merchants is None:
        merchants = generate_merchants(seed=seed)
    if profiles is None:
        profiles = generate_behavior_profiles(customers, seed=seed)

    cust_merged = customers.merge(profiles, on="customer_id")

    start_dt = pd.Timestamp(start_date)
    end_dt = pd.Timestamp(end_date)
    total_days = (end_dt - start_dt).days + 1
    dates = [start_dt + timedelta(days=i) for i in range(total_days)]

    transactions = []
    ground_truth = []
    tx_id_counter = 1

    domestic_merchants = merchants[merchants["country"] == "Spain"]
    intl_merchants = merchants[merchants["country"] != "Spain"]

    for current_date in dates:
        for _, cust in cust_merged.iterrows():
            p_daily = cust["latent_expected_transactions_month"] / 30.0
            n_tx_today = rng.poisson(lam=p_daily)

            for _ in range(n_tx_today):
                tx_id = f"TX_{start_dt.year}_{tx_id_counter:08d}"

                # 1. Normal Attribute Sampling
                is_online = bool(rng.random() < cust["latent_online_probability"])
                is_intl = bool(rng.random() < cust["latent_international_probability"])

                sigma = cust["latent_amount_variability"]
                mu = np.log(cust["latent_typical_transaction_amount"]) - (sigma**2 / 2)
                amount = max(round(float(rng.lognormal(mean=mu, sigma=sigma)), 2), 0.50)

                if is_intl and not intl_merchants.empty:
                    m_row = intl_merchants.sample(
                        1, random_state=rng.integers(0, 1000000)
                    ).iloc[0]
                else:
                    m_row = domestic_merchants.sample(
                        1, random_state=rng.integers(0, 1000000)
                    ).iloc[0]

                tx_timestamp = sample_transaction_time(
                    rng, current_date, cust["latent_night_probability"]
                )
                payment_method = sample_payment_method(rng, is_online)
                device_id = f"DEV_CUST_{cust['customer_id'][-5:]}_{rng.integers(1, cust['latent_number_of_devices'] + 1)}"

                # 2. Anomaly Injection
                is_anomaly = bool(rng.random() < anomaly_rate)
                anomaly_type = "None"
                is_fraud = False

                if is_anomaly:
                    anomaly_type = str(
                        rng.choice([
                            "HIGH_AMOUNT",
                            "UNUSUAL_NIGHT",
                            "NEW_FOREIGN_LOCATION",
                            "NEW_DEVICE_BURST",
                        ])
                    )

                    if anomaly_type == "HIGH_AMOUNT":
                        amount = round(amount * float(rng.uniform(8.0, 20.0)), 2)
                    elif anomaly_type == "UNUSUAL_NIGHT":
                        tx_timestamp = tx_timestamp.replace(hour=int(rng.integers(2, 5)))
                    elif anomaly_type == "NEW_FOREIGN_LOCATION":
                        if not intl_merchants.empty:
                            m_row = intl_merchants.sample(
                                1, random_state=rng.integers(0, 1000000)
                            ).iloc[0]
                        amount = round(amount * float(rng.uniform(2.0, 5.0)), 2)
                    elif anomaly_type == "NEW_DEVICE_BURST":
                        device_id = f"DEV_UNKNOWN_{rng.integers(9000, 9999)}"
                        amount = round(amount * float(rng.uniform(1.5, 4.0)), 2)

                    is_fraud = bool(rng.random() < 0.80)

                transactions.append({
                    "transaction_id": tx_id,
                    "customer_id": cust["customer_id"],
                    "merchant_id": m_row["merchant_id"],
                    "timestamp": tx_timestamp,
                    "amount": amount,
                    "currency": "EUR",
                    "country": m_row["country"],
                    "city": m_row["city"],
                    "device_id": device_id,
                    "payment_method": payment_method,
                    "is_online": is_online,
                    "transaction_type": "Online Payment" if is_online else "Card Payment",
                })

                ground_truth.append({
                    "transaction_id": tx_id,
                    "is_anomaly": is_anomaly,
                    "anomaly_type": anomaly_type,
                    "is_fraud": is_fraud,
                })

                tx_id_counter += 1

    return pd.DataFrame(transactions), pd.DataFrame(ground_truth)


# ============================================================
# SCRIPT EXECUTION
# ============================================================

if __name__ == "__main__":
    df_tx, df_gt = generate_transactions_for_range(
        start_date="2025-01-01",
        end_date="2025-01-31",
        anomaly_rate=0.015,
    )

    print("\nTransactions Sample:")
    print(df_tx.head())

    print("\nGround Truth Sample:")
    print(df_gt.head())

    print(f"\nTotal Transactions Generated: {len(df_tx):,}")