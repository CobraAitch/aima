from pydantic import BaseModel, field_validator

from aima.models.validators import check_budget_pct


class ChannelPlan(BaseModel):
    channel: str
    objective: str
    tactics: list[str]
    kpis: list[str]
    budget_pct: float

    @field_validator("budget_pct")
    @classmethod
    def _valid_budget_pct(cls, v: float) -> float:
        return check_budget_pct(v)


class MarketingStrategy(BaseModel):
    positioning: str
    value_proposition: str
    channel_plans: list[ChannelPlan] = []
    timeline_weeks: int = 8
    total_budget_recommendation: float = 0.0
