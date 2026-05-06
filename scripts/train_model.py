import warnings

import joblib
import pandas as pd
from sklearn.ensemble import AdaBoostClassifier, ExtraTreesClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier

from powerbot.app.core.config import get_settings
from powerbot.app.features.transformer import FeatureEngineer


warnings.filterwarnings("ignore")


def train() -> None:
    settings = get_settings()
    df = pd.read_csv(settings.raw_data_path).copy()
    if "t" in df.columns:
        df = df.drop(columns=["t"])

    df = df.replace({"Fault": {0: "No fault", 1: "LLLG fault", 2: "LG fault", 3: "LLG fault"}})
    X = df.drop(columns="Fault")
    y = df["Fault"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=234,
        stratify=y,
    )

    pipeline = Pipeline(
        [
            ("feature_engineering", FeatureEngineer(window=50, min_periods=1)),
            ("scaling", MinMaxScaler()),
            ("model", RandomForestClassifier()),
        ]
    )

    models = {
        "LogisticRegression": LogisticRegression(),
        "Random Forest": RandomForestClassifier(),
        "Decision Tree": DecisionTreeClassifier(),
        "K-Nearest Neighbours": KNeighborsClassifier(),
        "Naive Bayes": GaussianNB(),
        "Ada Boost": AdaBoostClassifier(),
        "Extra Trees": ExtraTreesClassifier(),
    }
    for model_name, model in models.items():
        model.fit(X_train, y_train)
        score = accuracy_score(y_test, model.predict(X_test))
        print(f"{model_name}: {score:.3f}")

    param_grid = {
        "model__n_estimators": [10, 20, 25],
        "model__max_depth": [10, 20, 25],
        "model__min_samples_split": [2, 5, 7],
        "model__min_samples_leaf": [1, 2, 4],
    }
    search = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=param_grid,
        n_iter=5,
        cv=5,
        verbose=2,
        random_state=234,
        n_jobs=1,
    )
    search.fit(X_train, y_train)
    joblib.dump(search.best_estimator_, settings.model_path)
    print(f"Saved trained pipeline to {settings.model_path}")


if __name__ == "__main__":
    train()
