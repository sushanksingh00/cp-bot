import pandas as pd
import numpy as np

def clean_data(
    input_path="ml/data/raw_dataset.csv",
    output_path="ml/data/cleaned_dataset.csv"
):
    print(f"Loading raw data from {input_path}...")

    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: Could not find {input_path}")
        return None

    initial_len = len(df)
    print(f"Initial record count: {initial_len}")

    # Required fields
    df = df.dropna(
        subset=[
            "submitted_at",
            "verdict",
            "user_id",
            "problem_index"
        ]
    )

    # Parse timestamp
    df["submitted_at"] = pd.to_datetime(
        df["submitted_at"],
        errors="coerce"
    )

    df = df.dropna(subset=["submitted_at"])

    # Problem rating must be valid
    df["problem_rating"] = pd.to_numeric(
        df["problem_rating"],
        errors="coerce"
    )

    df = df.dropna(subset=["problem_rating"])

    # Keep only valid positive ratings
    df = df[df["problem_rating"] > 0]

    # Sort chronologically
    df = df.sort_values(
        ["user_id", "submitted_at"]
    ).reset_index(drop=True)

    final_len = len(df)

    print(f"Records after cleaning: {final_len}")
    print(f"Removed {initial_len - final_len} invalid records.")

    # Validation
    assert not df["user_id"].isnull().any()
    assert not df["problem_rating"].isnull().any()
    assert not df["submitted_at"].isnull().any()

    df.to_csv(output_path, index=False)

    print(f"Cleaned dataset saved to {output_path}")

    return df


if __name__ == "__main__":
    clean_data()