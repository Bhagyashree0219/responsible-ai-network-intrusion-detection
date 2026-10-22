
import argparse
from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def main():
    parser = argparse.ArgumentParser(
        description="Explore unusual network traffic records."
    )
    parser.add_argument("--input", required=True, help="Input CSV file")
    parser.add_argument(
        "--output",
        default="results/anomaly_results.csv",
        help="Output CSV file",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        parser.error(f"CSV file not found: {input_path}")

    df = pd.read_csv(input_path)
    if df.empty:
        parser.error("The CSV file has no records.")

    features = df.select_dtypes(include="number").dropna(axis=1, how="all")
    if features.empty or len(features) < 2:
        parser.error("Provide at least two records and numeric features.")

    model = make_pipeline(
        SimpleImputer(strategy="median"),
        StandardScaler(),
        IsolationForest(
            n_estimators=100,
            contamination="auto",
            random_state=42,
        ),
    )

    predictions = model.fit_predict(features)

    results = df.copy()
    results["anomaly_flag"] = [
        "potential_anomaly" if value == -1 else "normal"
        for value in predictions
    ]

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_path, index=False)

    print(f"Records analyzed: {len(results)}")
    print(results["anomaly_flag"].value_counts().to_string())
    print(f"Results saved to: {output_path}")
    print("Potential anomalies require further investigation.")


if __name__ == "__main__":
    main()
