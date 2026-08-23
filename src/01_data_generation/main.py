from pathlib import Path

from config import (
    RAW_DATA_DIR,
)

from generate_customers import generate_customers


def main():

    # Create output directory if it does not exist
    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Customers
    # ------------s--------------------------------------------

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


if __name__ == "__main__":
    main()