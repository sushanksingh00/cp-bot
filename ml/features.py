import pandas as pd
import numpy as np
import json

from collections import defaultdict, deque
from datetime import timedelta


class UserState:
    """
    Maintains only information available BEFORE the current submission.

    This is critical for preventing target leakage during training.
    """

    def __init__(self, current_rating=1500):
        self.current_rating = current_rating

        # Overall history
        self.total_attempts = 0
        self.total_solved = 0
        self.solved_ratings = []

        # Tag-level history
        self.tag_attempts = defaultdict(int)
        self.tag_solved = defaultdict(int)

        # Recent attempts
        # (timestamp, solved, verdict)
        self.recent_attempts = deque()

        # Problem-specific history
        # key -> {"attempts": int, "solved": int, "failures": int}
        self.problem_history = defaultdict(
            lambda: {
                "attempts": 0,
                "solved": 0,
                "failures": 0
            }
        )

        # Verdict history
        self.verdict_counts = defaultdict(int)

        # Number of solved problems and attempts
        self.total_solved_problems = 0

        # Attempts required before solving a problem
        self.solve_attempt_counts = []

    # ---------------------------------------------------------
    # Update state AFTER generating features
    # ---------------------------------------------------------

    def update(
        self,
        problem_key,
        problem_rating,
        tags,
        verdict,
        timestamp
    ):
        solved = verdict == "OK"

        self.total_attempts += 1

        if solved:
            self.total_solved += 1
            self.total_solved_problems += 1

            if pd.notnull(problem_rating):
                self.solved_ratings.append(float(problem_rating))

        # -------------------------
        # Tags
        # -------------------------

        tags = parse_tags(tags)

        for tag in tags:
            self.tag_attempts[tag] += 1

            if solved:
                self.tag_solved[tag] += 1

        # -------------------------
        # Problem history
        # -------------------------

        history = self.problem_history[problem_key]

        history["attempts"] += 1

        if solved:
            history["solved"] += 1
        else:
            history["failures"] += 1

        # -------------------------
        # Verdict history
        # -------------------------

        self.verdict_counts[verdict] += 1

        # -------------------------
        # Recent history
        # -------------------------

        self.recent_attempts.append(
            (timestamp, solved, verdict)
        )

        self.cleanup_recent(timestamp)

        # -------------------------
        # Attempts before solve
        # -------------------------

        if solved:
            self.solve_attempt_counts.append(
                history["attempts"]
            )

    def cleanup_recent(self, timestamp):
        """
        Keep only the last 30 days of activity.
        """

        cutoff = timestamp - timedelta(days=30)

        while (
            self.recent_attempts
            and self.recent_attempts[0][0] < cutoff
        ):
            self.recent_attempts.popleft()


# =============================================================
# Utility functions
# =============================================================

def parse_tags(tags):
    """
    Convert tags_jsonb into a Python list safely.
    """

    if isinstance(tags, list):
        return tags

    if pd.isna(tags):
        return []

    if isinstance(tags, str):
        try:
            parsed = json.loads(tags)

            if isinstance(parsed, list):
                return parsed

        except Exception:
            pass

        # Handle simple PostgreSQL/string representations
        try:
            parsed = json.loads(
                tags.replace("'", '"')
            )

            if isinstance(parsed, list):
                return parsed

        except Exception:
            pass

    return []


def calculate_recent_features(state, timestamp):
    """
    Calculate recent behavioral features using only historical data.
    """

    cutoff_7 = timestamp - timedelta(days=7)
    cutoff_30 = timestamp - timedelta(days=30)

    recent_7 = []
    recent_30 = []

    for item in state.recent_attempts:
        ts, solved, verdict = item

        if ts >= cutoff_30:
            recent_30.append(item)

            if ts >= cutoff_7:
                recent_7.append(item)

    # -------------------------
    # 7 day
    # -------------------------

    recent_7_count = len(recent_7)

    recent_7_solved = sum(
        item[1] for item in recent_7
    )

    recent_7_solve_rate = (
        recent_7_solved / recent_7_count
        if recent_7_count > 0
        else 0.5
    )

    # -------------------------
    # 30 day
    # -------------------------

    recent_30_count = len(recent_30)

    recent_30_solved = sum(
        item[1] for item in recent_30
    )

    recent_30_solve_rate = (
        recent_30_solved / recent_30_count
        if recent_30_count > 0
        else 0.5
    )

    # -------------------------
    # Failure types
    # -------------------------

    if recent_30_count > 0:

        wrong_answer_rate = sum(
            item[2] == "WRONG_ANSWER"
            for item in recent_30
        ) / recent_30_count

        tle_rate = sum(
            item[2] == "TIME_LIMIT_EXCEEDED"
            for item in recent_30
        ) / recent_30_count

        runtime_error_rate = sum(
            item[2] == "RUNTIME_ERROR"
            for item in recent_30
        ) / recent_30_count

        compilation_error_rate = sum(
            item[2] == "COMPILATION_ERROR"
            for item in recent_30
        ) / recent_30_count

    else:
        wrong_answer_rate = 0.0
        tle_rate = 0.0
        runtime_error_rate = 0.0
        compilation_error_rate = 0.0

    return {
        "recent_7d_solve_rate": recent_7_solve_rate,
        "recent_7d_attempts": recent_7_count,
        "recent_30d_solve_rate": recent_30_solve_rate,
        "recent_30d_attempts": recent_30_count,
        "recent_wrong_answer_rate": wrong_answer_rate,
        "recent_tle_rate": tle_rate,
        "recent_runtime_error_rate": runtime_error_rate,
        "recent_compilation_error_rate": compilation_error_rate,
    }


# =============================================================
# Training feature generation
# =============================================================

def generate_features(
    df_path="ml/data/cleaned_dataset.csv",
    output_path="ml/data/features.csv"
):
    """
    Generate leakage-safe features.

    For every submission:

        historical data
              ↓
        calculate features
              ↓
        store target
              ↓
        update user state

    Therefore the current submission's outcome is NEVER used
    to calculate its own features.
    """

    print(f"Loading cleaned data from {df_path}...")

    try:
        df = pd.read_csv(df_path)

    except FileNotFoundError:
        print(f"Error: Could not find {df_path}")
        return None

    if df.empty:
        raise RuntimeError("Cleaned dataset is empty.")

    # ---------------------------------------------------------
    # Prepare data
    # ---------------------------------------------------------

    df["submitted_at"] = pd.to_datetime(
        df["submitted_at"],
        errors="coerce"
    )

    df["problem_rating"] = pd.to_numeric(
        df["problem_rating"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "submitted_at",
            "user_id",
            "problem_index",
            "problem_rating",
            "verdict"
        ]
    )

    # Chronological order is essential
    df = df.sort_values(
        ["user_id", "submitted_at", "id"]
    ).reset_index(drop=True)

    feature_rows = []
    user_states = {}

    print("Generating leakage-safe features...")

    for _, row in df.iterrows():

        user_id = row["user_id"]

        if user_id not in user_states:
            user_states[user_id] = UserState()

        state = user_states[user_id]

        timestamp = row["submitted_at"]
        problem_rating = float(row["problem_rating"])
        verdict = row["verdict"]

        tags = parse_tags(row["tags_jsonb"])

        # -----------------------------------------------------
        # Problem identifier
        # -----------------------------------------------------

        problem_key = (
            row["contest_id"],
            row["problem_index"]
        )

        problem_history = state.problem_history[
            problem_key
        ]

        # -----------------------------------------------------
        # 1. Overall historical performance
        # -----------------------------------------------------

        historical_solve_rate = (
            state.total_solved /
            state.total_attempts
            if state.total_attempts > 0
            else 0.5
        )

        total_attempts = state.total_attempts

        # -----------------------------------------------------
        # 2. Solved difficulty
        # -----------------------------------------------------

        avg_solved_rating = (
            np.mean(state.solved_ratings)
            if state.solved_ratings
            else 1500
        )

        max_solved_rating = (
            max(state.solved_ratings)
            if state.solved_ratings
            else 1500
        )

        # -----------------------------------------------------
        # 3. Difficulty difference
        # -----------------------------------------------------

        rating_difference = (
            avg_solved_rating -
            problem_rating
        )

        max_rating_difference = (
            max_solved_rating -
            problem_rating
        )

        # -----------------------------------------------------
        # 4. Tag performance
        # -----------------------------------------------------

        tag_familiarities = []
        tag_success_rates = []

        for tag in tags:

            attempts = state.tag_attempts.get(
                tag,
                0
            )

            solved = state.tag_solved.get(
                tag,
                0
            )

            tag_familiarities.append(
                attempts
            )

            if attempts > 0:
                tag_success_rates.append(
                    solved / attempts
                )

        avg_tag_familiarity = (
            np.mean(tag_familiarities)
            if tag_familiarities
            else 0
        )

        avg_tag_success = (
            np.mean(tag_success_rates)
            if tag_success_rates
            else historical_solve_rate
        )

        strongest_tag_success = (
            max(tag_success_rates)
            if tag_success_rates
            else historical_solve_rate
        )

        weakest_tag_success = (
            min(tag_success_rates)
            if tag_success_rates
            else historical_solve_rate
        )

        # -----------------------------------------------------
        # 5. Recent behavior
        # -----------------------------------------------------

        recent_features = calculate_recent_features(
            state,
            timestamp
        )

        # -----------------------------------------------------
        # 6. Same-problem history
        # -----------------------------------------------------

        previous_problem_attempts = (
            problem_history["attempts"]
        )

        previous_problem_failures = (
            problem_history["failures"]
        )

        previous_problem_solved = (
            problem_history["solved"]
        )

        # -----------------------------------------------------
        # 7. Historical attempts-before-solving
        # -----------------------------------------------------

        avg_attempts_before_solve = (
            np.mean(state.solve_attempt_counts)
            if state.solve_attempt_counts
            else 1.0
        )

        # -----------------------------------------------------
        # 8. Activity intensity
        # -----------------------------------------------------

        recent_30d_attempts = (
            recent_features["recent_30d_attempts"]
        )

        # -----------------------------------------------------
        # Create feature row
        # -----------------------------------------------------

        features = {

            # Identifiers
            "id": row["id"],
            "user_id": user_id,
            "submitted_at": row["submitted_at"],

            # Problem
            "problem_rating": problem_rating,

            # Difficulty
            "rating_difference": rating_difference,
            "max_rating_difference": max_rating_difference,
            "avg_solved_rating": avg_solved_rating,
            "max_solved_rating": max_solved_rating,

            # Overall performance
            "historical_solve_rate": historical_solve_rate,
            "total_attempts": total_attempts,

            # Tags
            "avg_tag_familiarity": avg_tag_familiarity,
            "avg_tag_success": avg_tag_success,
            "strongest_tag_success": strongest_tag_success,
            "weakest_tag_success": weakest_tag_success,

            # Recent performance
            "recent_7d_solve_rate":
                recent_features[
                    "recent_7d_solve_rate"
                ],

            "recent_7d_attempts":
                recent_features[
                    "recent_7d_attempts"
                ],

            "recent_30d_solve_rate":
                recent_features[
                    "recent_30d_solve_rate"
                ],

            "recent_30d_attempts":
                recent_features[
                    "recent_30d_attempts"
                ],

            # Failure behavior
            "recent_wrong_answer_rate":
                recent_features[
                    "recent_wrong_answer_rate"
                ],

            "recent_tle_rate":
                recent_features[
                    "recent_tle_rate"
                ],

            "recent_runtime_error_rate":
                recent_features[
                    "recent_runtime_error_rate"
                ],

            "recent_compilation_error_rate":
                recent_features[
                    "recent_compilation_error_rate"
                ],

            # Same problem
            "previous_problem_attempts":
                previous_problem_attempts,

            "previous_problem_failures":
                previous_problem_failures,

            "previous_problem_solved":
                previous_problem_solved,

            # Solving behavior
            "avg_attempts_before_solve":
                avg_attempts_before_solve,

            # Target
            "solved":
                1 if verdict == "OK" else 0
        }

        feature_rows.append(features)

        # -----------------------------------------------------
        # UPDATE STATE ONLY AFTER FEATURE GENERATION
        # -----------------------------------------------------

        state.update(
            problem_key=problem_key,
            problem_rating=problem_rating,
            tags=tags,
            verdict=verdict,
            timestamp=timestamp
        )

    features_df = pd.DataFrame(feature_rows)

    # Replace numerical infinities
    features_df = features_df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    # Fill numerical missing values
    numeric_columns = features_df.select_dtypes(
        include=[np.number]
    ).columns

    features_df[numeric_columns] = (
        features_df[numeric_columns]
        .fillna(0)
    )

    features_df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Features generated and saved to "
        f"{output_path} ({len(features_df)} rows)."
    )

    print(
        f"Feature count: "
        f"{len(features_df.columns)} columns"
    )

    return features_df


# =============================================================
# Live inference
# =============================================================

def get_inference_features(
    user_id,
    problem_rating,
    tags,
    session
):
    """
    Generate features for a new problem using the user's
    historical submissions.

    IMPORTANT:
    The current problem's result is not included.
    """

    from models import ProblemAttempt

    attempts = (
        session.query(ProblemAttempt)
        .filter(
            ProblemAttempt.user_id == user_id
        )
        .order_by(
            ProblemAttempt.submitted_at
        )
        .all()
    )

    state = UserState()

    for row in attempts:

        problem_key = (
            row.contest_id,
            row.problem_index
        )

        state.update(
            problem_key=problem_key,
            problem_rating=row.problem_rating,
            tags=row.tags_jsonb,
            verdict=row.verdict,
            timestamp=row.submitted_at
        )

    now = pd.Timestamp.utcnow().tz_localize(None)

    # ---------------------------------------------------------
    # Overall
    # ---------------------------------------------------------

    historical_solve_rate = (
        state.total_solved /
        state.total_attempts
        if state.total_attempts > 0
        else 0.5
    )

    avg_solved_rating = (
        np.mean(state.solved_ratings)
        if state.solved_ratings
        else 1500
    )

    max_solved_rating = (
        max(state.solved_ratings)
        if state.solved_ratings
        else 1500
    )

    if problem_rating is None:
        problem_rating = 1500

    rating_difference = (
        avg_solved_rating -
        problem_rating
    )

    max_rating_difference = (
        max_solved_rating -
        problem_rating
    )

    # ---------------------------------------------------------
    # Tags
    # ---------------------------------------------------------

    tags = parse_tags(tags)

    tag_familiarities = []
    tag_success_rates = []

    for tag in tags:

        attempts_t = state.tag_attempts.get(
            tag,
            0
        )

        solved_t = state.tag_solved.get(
            tag,
            0
        )

        tag_familiarities.append(
            attempts_t
        )

        if attempts_t > 0:
            tag_success_rates.append(
                solved_t / attempts_t
            )

    avg_tag_familiarity = (
        np.mean(tag_familiarities)
        if tag_familiarities
        else 0
    )

    avg_tag_success = (
        np.mean(tag_success_rates)
        if tag_success_rates
        else historical_solve_rate
    )

    strongest_tag_success = (
        max(tag_success_rates)
        if tag_success_rates
        else historical_solve_rate
    )

    weakest_tag_success = (
        min(tag_success_rates)
        if tag_success_rates
        else historical_solve_rate
    )

    # ---------------------------------------------------------
    # Recent
    # ---------------------------------------------------------

    recent_features = calculate_recent_features(
        state,
        now
    )

    # ---------------------------------------------------------
    # Return exactly the feature set used by training
    # ---------------------------------------------------------

    features = {

        "problem_rating": problem_rating,

        "rating_difference":
            rating_difference,

        "max_rating_difference":
            max_rating_difference,

        "avg_solved_rating":
            avg_solved_rating,

        "max_solved_rating":
            max_solved_rating,

        "historical_solve_rate":
            historical_solve_rate,

        "total_attempts":
            state.total_attempts,

        "avg_tag_familiarity":
            avg_tag_familiarity,

        "avg_tag_success":
            avg_tag_success,

        "strongest_tag_success":
            strongest_tag_success,

        "weakest_tag_success":
            weakest_tag_success,

        "recent_7d_solve_rate":
            recent_features[
                "recent_7d_solve_rate"
            ],

        "recent_7d_attempts":
            recent_features[
                "recent_7d_attempts"
            ],

        "recent_30d_solve_rate":
            recent_features[
                "recent_30d_solve_rate"
            ],

        "recent_30d_attempts":
            recent_features[
                "recent_30d_attempts"
            ],

        "recent_wrong_answer_rate":
            recent_features[
                "recent_wrong_answer_rate"
            ],

        "recent_tle_rate":
            recent_features[
                "recent_tle_rate"
            ],

        "recent_runtime_error_rate":
            recent_features[
                "recent_runtime_error_rate"
            ],

        "recent_compilation_error_rate":
            recent_features[
                "recent_compilation_error_rate"
            ],

        # No exact-problem history is supplied here because
        # inference may be for a problem not previously attempted.
        "previous_problem_attempts": 0,
        "previous_problem_failures": 0,
        "previous_problem_solved": 0,

        "avg_attempts_before_solve": (
            np.mean(state.solve_attempt_counts)
            if state.solve_attempt_counts
            else 1.0
        )
    }

    # Final validation to match training's fillna(0) and replace(inf, nan)
    for k, v in features.items():
        if v is None or pd.isna(v) or np.isinf(v):
            features[k] = 0.0

    return features


if __name__ == "__main__":
    generate_features()