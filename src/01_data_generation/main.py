from pathlib import Path

from config import (
    RAW_DATA_DIR,
)

from generate_customers import generate_customers
from generate_merchants import generate_merchants


def main():

    # Create output directory if it does not exist
    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ========================================================
    # Customers
    # ========================================================

    print("Generating customers...")

    customers = generate_customers()

    customers.to_csv(
        RAW_DATA_DIR / "customers.csv",
        index=False,
    )

    print(
        f"Generated {len(customers):,} customers."
    )

    print(
        f"Saved to: {RAW_DATA_DIR / 'customers.csv'}"
    )

    # ========================================================
    # MERCHANTS
    # ========================================================

    print("\nGenerating merchants...")

    merchants = generate_merchants()

    merchants.to_csv(
        RAW_DATA_DIR / "merchants.csv",
        index=False,
    )

    print(
        f"Generated {len(merchants):,} merchants."
    )

    print("\nData generation completed.")


if __name__ == "__main__":
    main()