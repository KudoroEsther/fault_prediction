"""Compatibility shim for legacy pickled sklearn pipelines.

The saved model artifact was trained when ``FeatureEngineer`` lived in the
root-level ``Feature_engineer`` module. Joblib imports that module path during
deserialization, so we keep this thin re-export in place until the model is
retrained and saved from the new package path.
"""

from powerbot.app.features.transformer import FeatureEngineer

__all__ = ["FeatureEngineer"]
