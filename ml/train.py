import os
import pandas as pd
import numpy as np
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
)
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


def train_and_evaluate(
    features_path="ml/data/features.csv",
    models_dir="ml/models",
):
    print(f"Loading features from {features_path}...")

    try:
        df = pd.read_csv(features_path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Could not find {features_path}. "
            "Run ml/features.py first."
        )

    if df.empty:
        raise RuntimeError("Feature dataset is empty.")

    os.makedirs(models_dir, exist_ok=True)

    # =========================================================
    # 1. Clean feature dataset
    # =========================================================

    df = df.replace([np.inf, -np.inf], np.nan)

    # submitted_at is needed for temporal splitting
    df["submitted_at"] = pd.to_datetime(
        df["submitted_at"],
        errors="coerce",
    )

    df = df.dropna(
        subset=[
            "submitted_at",
            "solved",
        ]
    )

    # Sort globally by actual submission time.
    # This prevents future submissions from entering training.
    df = df.sort_values(
        "submitted_at"
    ).reset_index(drop=True)

    print(f"\nDataset after cleanup: {len(df)} rows")

    # =========================================================
    # 2. Select ML features
    # =========================================================

    # These columns are NOT model features.
    #
    # id          -> database identifier
    # user_id     -> user identifier
    # submitted_at -> temporal metadata
    # solved      -> target variable
    #
    # Using user_id or id would allow the model to memorize
    # identities rather than learn solving behavior.

    excluded_columns = {
        "id",
        "user_id",
        "submitted_at",
        "solved",
    }

    feature_cols = [
        column
        for column in df.columns
        if column not in excluded_columns
    ]

    target_col = "solved"

    X = df[feature_cols].copy()
    y = df[target_col].astype(int)

    # Make sure all model inputs are numeric.
    X = X.apply(
        pd.to_numeric,
        errors="coerce",
    )

    # Remove rows that became invalid after conversion.
    valid_rows = X.notna().all(axis=1)

    X = X.loc[valid_rows].reset_index(drop=True)
    y = y.loc[valid_rows].reset_index(drop=True)

    # Keep dataframe aligned with X/y for temporal reporting.
    df = df.loc[valid_rows].reset_index(drop=True)

    print(f"Dataset shape: {X.shape}")
    print(f"Number of features: {len(feature_cols)}")

    print("\nFeatures used:")
    for feature in feature_cols:
        print(f"  - {feature}")

    print("\nClass distribution:")
    print(y.value_counts())

    print("\nClass distribution (%):")
    print(
        y.value_counts(normalize=True)
    )

    # =========================================================
    # 3. TRUE TEMPORAL TRAIN / TEST SPLIT
    # =========================================================

    split_index = int(len(df) * 0.80)

    train_df = df.iloc[:split_index]
    test_df = df.iloc[split_index:]

    X_train = train_df[feature_cols]
    X_test = test_df[feature_cols]

    y_train = train_df[target_col].astype(int)
    y_test = test_df[target_col].astype(int)

    print("\n" + "=" * 70)
    print("TEMPORAL TRAIN / TEST SPLIT")
    print("=" * 70)

    print(f"Training rows: {len(X_train)}")
    print(f"Testing rows:  {len(X_test)}")

    print(
        f"\nTraining period:\n"
        f"{train_df['submitted_at'].min()} "
        f"→ "
        f"{train_df['submitted_at'].max()}"
    )

    print(
        f"\nTesting period:\n"
        f"{test_df['submitted_at'].min()} "
        f"→ "
        f"{test_df['submitted_at'].max()}"
    )

    # Safety check:
    # The latest training submission must be earlier than
    # the earliest testing submission.
    if (
        train_df["submitted_at"].max()
        > test_df["submitted_at"].min()
    ):
        raise RuntimeError(
            "Temporal split failed: training data contains "
            "timestamps after testing data."
        )

    # =========================================================
    # 4. Majority-class baseline
    # =========================================================

    majority_class = y_train.mode()[0]

    baseline_pred = np.full(
        len(y_test),
        majority_class,
    )

    baseline_accuracy = accuracy_score(
        y_test,
        baseline_pred,
    )

    print("\n" + "=" * 70)
    print("BASELINE")
    print("=" * 70)

    print(
        f"Majority class: {majority_class}"
    )

    print(
        f"Baseline accuracy: "
        f"{baseline_accuracy:.4f}"
    )

    # =========================================================
    # 5. Models
    # =========================================================

    models = {
        "Logistic Regression": Pipeline(
            [
                (
                    "scaler",
                    StandardScaler(),
                ),
                (
                    "model",
                    LogisticRegression(
                        max_iter=2000,
                        class_weight="balanced",
                        random_state=42,
                    ),
                ),
            ]
        ),

        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            max_depth=12,
            min_samples_leaf=5,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ),
    }

    # =========================================================
    # 6. Train and evaluate
    # =========================================================

    results = []

    best_score = -np.inf
    best_model = None
    best_model_name = ""

    print("\n" + "=" * 70)
    print("MODEL TRAINING")
    print("=" * 70)

    for name, model in models.items():

        print(f"\nTraining {name}...")

        model.fit(
            X_train,
            y_train,
        )

        # Predictions
        y_pred = model.predict(
            X_test
        )

        # Probability of solving
        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(
                X_test
            )[:, 1]
        else:
            y_prob = y_pred

        # -----------------------------------------------------
        # Metrics
        # -----------------------------------------------------

        accuracy = accuracy_score(
            y_test,
            y_pred,
        )

        precision = precision_score(
            y_test,
            y_pred,
            zero_division=0,
        )

        recall = recall_score(
            y_test,
            y_pred,
            zero_division=0,
        )

        f1 = f1_score(
            y_test,
            y_pred,
            zero_division=0,
        )

        roc_auc = roc_auc_score(
            y_test,
            y_prob,
        )

        pr_auc = average_precision_score(
            y_test,
            y_prob,
        )

        cm = confusion_matrix(
            y_test,
            y_pred,
        )

        results.append(
            {
                "Model": name,
                "Accuracy": accuracy,
                "Precision": precision,
                "Recall": recall,
                "F1": f1,
                "ROC-AUC": roc_auc,
                "PR-AUC": pr_auc,
            }
        )

        # -----------------------------------------------------
        # Print metrics
        # -----------------------------------------------------

        print(
            f"Accuracy:  {accuracy:.4f}"
        )

        print(
            f"Precision: {precision:.4f}"
        )

        print(
            f"Recall:    {recall:.4f}"
        )

        print(
            f"F1:        {f1:.4f}"
        )

        print(
            f"ROC-AUC:   {roc_auc:.4f}"
        )

        print(
            f"PR-AUC:    {pr_auc:.4f}"
        )

        print("\nConfusion Matrix:")

        print(
            "                 Predicted"
        )

        print(
            "                 0       1"
        )

        print(
            f"Actual 0       {cm[0, 0]:5d}  {cm[0, 1]:5d}"
        )

        print(
            f"Actual 1       {cm[1, 0]:5d}  {cm[1, 1]:5d}"
        )

        # -----------------------------------------------------
        # Model selection
        #
        # ROC-AUC measures ranking quality and is more useful
        # than raw accuracy for this imbalanced classification
        # problem.
        # -----------------------------------------------------

        if roc_auc > best_score:
            best_score = roc_auc
            best_model = model
            best_model_name = name

    # =========================================================
    # 7. Model comparison
    # =========================================================

    results_df = pd.DataFrame(
        results
    )

    print("\n" + "=" * 70)
    print("MODEL COMPARISON")
    print("=" * 70)

    print(
        results_df.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )

    # =========================================================
    # 8. Save best model
    # =========================================================

    if best_model is None:
        raise RuntimeError(
            "No model was successfully trained."
        )

    model_path = os.path.join(
        models_dir,
        "best_model.pkl",
    )

    joblib.dump(
        best_model,
        model_path,
    )

    # Save feature names.
    # inference_services.py should use this file so that
    # inference always follows the same feature ordering.
    feature_cols_path = os.path.join(
        models_dir,
        "feature_cols.pkl",
    )

    joblib.dump(
        feature_cols,
        feature_cols_path,
    )

    print(
        f"\nSelected model: {best_model_name}"
    )

    print(
        f"Model saved to: {model_path}"
    )

    print(
        f"Feature list saved to: {feature_cols_path}"
    )

    # =========================================================
    # 9. Feature importance
    # =========================================================

    print("\n" + "=" * 70)
    print("FEATURE IMPORTANCE")
    print("=" * 70)

    if best_model_name == "Random Forest":

        importances = (
            best_model.feature_importances_
        )

    elif best_model_name == "Logistic Regression":

        classifier = (
            best_model
            .named_steps["model"]
        )

        # Absolute coefficient magnitude
        # indicates how strongly each feature influences
        # the prediction.
        importances = np.abs(
            classifier.coef_[0]
        )

    else:
        importances = np.zeros(
            len(feature_cols)
        )

    importance_df = pd.DataFrame(
        {
            "Feature": feature_cols,
            "Importance": importances,
        }
    )

    importance_df = importance_df.sort_values(
        by="Importance",
        ascending=False,
    )

    print(
        importance_df.to_string(
            index=False
        )
    )

    importance_path = os.path.join(
        models_dir,
        "feature_importance.csv",
    )

    importance_df.to_csv(
        importance_path,
        index=False,
    )

    # =========================================================
    # 10. Save model comparison
    # =========================================================

    results_path = os.path.join(
        models_dir,
        "model_comparison.csv",
    )

    results_df.to_csv(
        results_path,
        index=False,
    )

    print(
        f"\nModel comparison saved to: "
        f"{results_path}"
    )

    print(
        f"Feature importance saved to: "
        f"{importance_path}"
    )

    print("\nTraining complete.")

    return results_df


if __name__ == "__main__":
    train_and_evaluate()