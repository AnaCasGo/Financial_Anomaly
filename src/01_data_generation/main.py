from config import (
    BEHAVIOR_PROFILE_PATH,
    HISTORICAL_ANOMALY_RATE,
    HISTORICAL_END,
    HISTORICAL_START,
    PRODUCTION_ANOMALY_RATE,
    PRODUCTION_END,
    PRODUCTION_START,
    PROCESSED_DATA_DIR,
    RANDOM_SEED,
    RAW_DATA_DIR,
)
from generate_behaviour_profiles import generate_behavior_profiles
from generate_customers import generate_customers
from generate_merchants import generate_merchants
from generate_transactions import generate_transactions_for_range


def main():

    # Create output directory if it does not exist
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # ========================================================
    # Customers
    # ========================================================
    
    print("Generating customers...")
    customers = generate_customers()
    customers.to_csv(RAW_DATA_DIR / "customers.csv", index=False)
    print(f"Saved {len(customers):,} customers to {RAW_DATA_DIR / 'customers.csv'}")

    # ========================================================
    # MERCHANTS
    # ========================================================

    print("\nGenerating merchants...")
    merchants = generate_merchants()
    merchants.to_csv(RAW_DATA_DIR / "merchants.csv", index=False)
    print(f"Saved {len(merchants):,} merchants to {RAW_DATA_DIR / 'merchants.csv'}")

    # ========================================================
    # LATENT BEHAVIORAL PROFILES
    # ========================================================

    print("\nGenerating latent behavior profiles...")
    profiles = generate_behavior_profiles(customers)
    profiles.to_csv(BEHAVIOR_PROFILE_PATH, index=False)
    print(f"Saved profiles to {BEHAVIOR_PROFILE_PATH}")

    # ========================================================
    # TRANSACTIONS & GROUND TRUTH
    # ========================================================

    print("\nGenerating HISTORICAL transactions batch...")

    df_tx_hist, df_gt_hist = generate_transactions_for_range(
        start_date=HISTORICAL_START,
        end_date=HISTORICAL_END,
        anomaly_rate=HISTORICAL_ANOMALY_RATE,
        customers=customers,
        merchants=merchants,
        profiles=profiles,
        seed=RANDOM_SEED,
    )

    df_tx_hist.to_csv(RAW_DATA_DIR / "transactions_historical.csv", index=False)
    df_gt_hist.to_csv(PROCESSED_DATA_DIR / "ground_truth_historical.csv", index=False)

    print(f"Saved {len(df_tx_hist):,} historical transactions.")

    # ========================================================
    # PRODUCTION TRANSACTIONS BATCH
    # ========================================================

    print("\nGenerating PRODUCTION transactions batch...")

    df_tx_prod, df_gt_prod = generate_transactions_for_range(
        start_date=PRODUCTION_START,
        end_date=PRODUCTION_END,
        anomaly_rate=PRODUCTION_ANOMALY_RATE,
        customers=customers,
        merchants=merchants,
        profiles=profiles,
        seed=RANDOM_SEED + 1,
    )

    df_tx_prod.to_csv(RAW_DATA_DIR / "transactions_production.csv", index=False)
    df_gt_prod.to_csv(PROCESSED_DATA_DIR / "ground_truth_production.csv", index=False)

    print(f"Saved {len(df_tx_prod):,} production transactions.")

    print("\nData generation pipeline completed successfully.")


if __name__ == "__main__":
    main()