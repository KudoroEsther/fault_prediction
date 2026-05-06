import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class FeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(self, window: int = 50, min_periods: int = 1):
        self.window = window
        self.min_periods = min_periods
        self.volt_cols = ["Va", "Vb", "Vc"]
        self.curr_cols = ["Ia", "Ib", "Ic"]
        self.all_cols = self.volt_cols + self.curr_cols

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = pd.DataFrame(X).copy()

        for col in self.all_cols:
            df[f"{col}_rms"] = df[col].rolling(
                self.window,
                min_periods=self.min_periods,
            ).apply(lambda values: np.sqrt(np.mean(values**2)), raw=True)

        for col in self.all_cols:
            df[f"{col}_ptp"] = df[col].rolling(
                self.window,
                min_periods=self.min_periods,
            ).apply(np.ptp, raw=True)

        df["Vab"] = df["Va"] - df["Vb"]
        df["Vbc"] = df["Vb"] - df["Vc"]
        df["Vca"] = df["Vc"] - df["Va"]

        df["Iab"] = df["Ia"] - df["Ib"]
        df["Ibc"] = df["Ib"] - df["Ic"]
        df["Ica"] = df["Ic"] - df["Ia"]

        df["P_total"] = (
            df["Va"] * df["Ia"]
            + df["Vb"] * df["Ib"]
            + df["Vc"] * df["Ic"]
        )
        return df
