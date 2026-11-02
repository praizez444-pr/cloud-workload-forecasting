import numpy as np
import pandas as pd
from pathlib import Path


def main():
    # Locate the project directory
    project_dir = Path(__file__).resolve().parent.parent

    # Load the source datasets
    cpu_path = project_dir / "challenge_data" / "vm_cpu_readings.csv.gz"
    metadata_path = project_dir / "challenge_data" / "vm_metadata.csv.gz"

    cpu_df = pd.read_csv(cpu_path)
    metadata_df = pd.read_csv(metadata_path)

    # Aggregate VM readings by timestamp
    aggregate_df = (
        cpu_df.groupby("timestamp")
        .agg(
            active_vm_count=("vm_id", "nunique"),
            aggregate_cpu_utilization=("avg_cpu", "mean")
        )
        .reset_index()
        .sort_values("timestamp")
        .reset_index(drop=True)
    )

    # Split development and holdout observations
    train_df = aggregate_df.iloc[:110].copy()
    holdout_df = aggregate_df.iloc[110:].copy()

    if len(train_df) != 110 or len(holdout_df) != 24:
        raise ValueError("Expected 110 development and 24 holdout observations.")

    # Forecast active VM count using the last observed value
    predicted_active_vm_count = train_df["active_vm_count"].iloc[-1]

    # Forecast CPU utilization using the last 6 observations
    predicted_cpu_utilization = (
        train_df["aggregate_cpu_utilization"].tail(6).mean()
    )

    # Generate forecasts for the holdout timestamps
    predictions_df = pd.DataFrame({
        "timestamp": holdout_df["timestamp"].values,
        "active_vm_count": predicted_active_vm_count,
        "aggregate_cpu_utilization": predicted_cpu_utilization
    })

    # Validate predictions
    assert len(predictions_df) == 24
    assert list(predictions_df.columns) == [
        "timestamp",
        "active_vm_count",
        "aggregate_cpu_utilization"
    ]
    assert np.array_equal(
        predictions_df["timestamp"].values,
        holdout_df["timestamp"].values
    )
    assert np.isfinite(
        predictions_df.select_dtypes(include="number")
    ).all().all()
    assert (predictions_df["active_vm_count"] >= 0).all()
    assert predictions_df["aggregate_cpu_utilization"].between(0, 100).all()

    # Save predictions
    output_path = project_dir / "predictions.csv"
    predictions_df.to_csv(output_path, index=False)

    print("Forecasting completed successfully!")
    print(f"Predictions saved to: {output_path}")
    print(predictions_df.head())


if __name__ == "__main__":
    main()
