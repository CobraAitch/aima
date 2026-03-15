"""Shared field validators used across multiple models."""


def check_budget_pct(v: float) -> float:
    if not 0 <= v <= 100:
        raise ValueError(f"budget_pct must be 0-100, got {v}")
    return v
