import pandas as pd

from powerbot.app.features.transformer import FeatureEngineer


def test_feature_engineer_adds_expected_columns():
    df = pd.DataFrame(
        [
            {"Va": 220.0, "Vb": 219.0, "Vc": 221.0, "Ia": 10.0, "Ib": 11.0, "Ic": 9.5},
            {"Va": 218.0, "Vb": 220.0, "Vc": 222.0, "Ia": 10.5, "Ib": 11.5, "Ic": 9.0},
        ]
    )

    transformed = FeatureEngineer(window=2).fit_transform(df)

    for column in ["Va_rms", "Ia_ptp", "Vab", "Ica", "P_total"]:
        assert column in transformed.columns
